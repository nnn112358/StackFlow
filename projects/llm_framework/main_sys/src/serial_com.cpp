/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include "serial.h"

#include <unistd.h>

#include <chrono>
#include <cstring>
#include <ctime>
#include <iostream>
#include <list>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
#include <fstream>
#include <cstdio>

#include "all.h"
#include "event_loop.h"
#include "zmq_bus.h"
#include "linux_uart/linux_uart.h"
#include <memory>

class serial_com : public zmq_bus_com {
   private:
    int uart_fd;

   public:
    serial_com(uart_t *uart_parm, const std::string &dev_name) : zmq_bus_com() {
        uart_fd = linux_uart_init((char *)dev_name.c_str(), uart_parm);
        if (uart_fd <= 0) {
            SLOGE("open %s false!", dev_name.c_str());
            exit(-1);
        }
    }

    void send_data(const std::string &data) {
        SLOGD("serial send:%s", data.c_str());
        linux_uart_write(uart_fd, data.length(), (void *)data.c_str());
    }

    void reace_data_event() {
        std::string json_str;
        int flage = 0;
        fd_set readfds;
        while (exit_flage) {
            char reace_buf[128] = {0};
            FD_ZERO(&readfds);
            FD_SET(uart_fd, &readfds);
            struct timeval timeout = {0, 500000};
            if ((select(uart_fd + 1, &readfds, NULL, NULL, &timeout) <= 0) || (!FD_ISSET(uart_fd, &readfds))) continue;
            int len = linux_uart_read(uart_fd, 128, reace_buf);
            {
                char *data = reace_buf;
                for (int i = 0; i < len; i++) {
                    json_str += data[i];
                    if (data[i] == '{') flage++;
                    if (data[i] == '}') flage--;
                    if (flage == 0) {
                        if (json_str[0] == '{') {
                            SLOGD("uart reace:%s", json_str.c_str());
                            on_data(json_str);
                        }
                        json_str.clear();
                    }
                    if (flage < 0) {
                        flage = 0;
                        json_str.clear();
                        {
                            std::string out_str;
                            out_str += "{\"request_id\": \"0\",\"work_id\": \"sys\",\"created\": ";
                            out_str += std::to_string(time(NULL));
                            out_str += ",\"error\":{\"code\":-1, \"message\":\"reace reset\"}}";
                            send_data(out_str);
                        }
                    }
                }
            }
        }
    }

    void stop() {
        zmq_bus_com::stop();
        linux_uart_deinit(uart_fd);
    }
    
    ~serial_com() {
        if (exit_flage) {
            stop();
        }
    }
};
std::unique_ptr<serial_com> serial_con_;

void serial_work() {
    uart_t uart_parm;
    std::string dev_name;
    int port;
    memset(&uart_parm, 0, sizeof(uart_parm));
    SAFE_READING(uart_parm.baud, int, "config_serial_baud");
    SAFE_READING(uart_parm.data_bits, int, "config_serial_data_bits");
    SAFE_READING(uart_parm.stop_bits, int, "config_serial_stop_bits");
    SAFE_READING(uart_parm.parity, int, "config_serial_parity");
    SAFE_READING(dev_name, std::string, "config_serial_dev");
    SAFE_READING(port, int, "config_serial_zmq_port");

    serial_con_ = std::make_unique<serial_com>(&uart_parm, dev_name);
    serial_con_->work(zmq_s_format, port);

    if (access("/var/llm_update.lock", F_OK) == 0) {
        remove("/var/llm_update.lock");
        sync();
        std::string out_str;
        out_str += "{\"request_id\": \"0\",\"work_id\": \"sys\",\"created\": ";
        out_str += std::to_string(time(NULL));
        out_str += ",\"error\":{\"code\":0, \"message\":\"upgrade over\"}}";
        serial_con_->send_data(out_str);
    }
    if (access("/tmp/llm/reset.lock", F_OK) == 0) {
        remove("/tmp/llm/reset.lock");
        sync();
        std::string out_str;
        out_str += "{\"request_id\": \"0\",\"work_id\": \"sys\",\"created\": ";
        out_str += std::to_string(time(NULL));
        out_str += ",\"error\":{\"code\":0, \"message\":\"reset over\"}}";
        serial_con_->send_data(out_str);
    }
    sync();
}

void serial_stop_work() {
    serial_con_.reset();
}
