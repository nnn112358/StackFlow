#!/bin/env python3
import os
import sys
import shutil
import subprocess
import requests
import tarfile
import shutil
'''
{package_name}_{version}-{revision}_{architecture}.deb
lib-llm_1.0-m5stack1_arm64.deb
llm-sys_1.0-m5stack1_arm64.deb
llm-audio_1.0-m5stack1_arm64.deb
llm-kws_1.0-m5stack1_arm64.deb
llm-asr_1.0-m5stack1_arm64.deb
llm-llm_1.0-m5stack1_arm64.deb
llm-tts_1.0-m5stack1_arm64.deb
'''


def create_lib_deb(package_name, version, src_folder, revision = 'm5stack1'):
    deb_file = f"{package_name}_{version}-{revision}_arm64.deb"
    deb_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debian')
    if os.path.exists(deb_folder):
        shutil.rmtree(deb_folder)
    os.makedirs(deb_folder, exist_ok = True)
    
    for item in os.listdir(src_folder):
        if item.startswith('llm_'):
            continue
        elif item.startswith('lib'):
            os.makedirs(os.path.join(deb_folder, 'opt/m5stack/lib'), exist_ok = True)
            shutil.copy2(os.path.join(src_folder, item), os.path.join(deb_folder, 'opt/m5stack/lib', item))
        else:
            os.makedirs(os.path.join(deb_folder, 'opt/m5stack/share'), exist_ok = True)
            shutil.copy2(os.path.join(src_folder, item), os.path.join(deb_folder, 'opt/m5stack/share', item))
    # os.makedirs(os.path.join(deb_folder, 'opt/m5stack/data'), exist_ok = True)

    zip_file = 'm5stack_scripts.tar.gz'
    down_url = 'https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/linux/llm/m5stack_scripts.tar.gz'
    zip_file_extrpath = 'm5stack_scripts'
    if not os.path.exists(zip_file_extrpath):
        # Downloading via HTTP (more common)
        if not os.path.exists(zip_file):
            response = requests.get(down_url)
            if response.status_code == 200:
                with open(zip_file, 'wb') as file:
                    file.write(response.content)
            else:
                print("{} down failed".format(down_url))
        with tarfile.open(zip_file, 'r:gz') as tar:
            tar.extractall(path=zip_file_extrpath)
        print("The {} download successful.".format(down_url))
    if os.path.exists(zip_file_extrpath):
        shutil.copytree(zip_file_extrpath, os.path.join(deb_folder, 'opt/m5stack/scripts'))

    zip_file = 'm5stack_dist-packages.tar.gz'
    down_url = 'https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/linux/llm/m5stack_dist-packages.tar.gz'
    zip_file_extrpath = 'm5stack_dist-packages'
    if not os.path.exists(zip_file_extrpath):
        # Downloading via HTTP (more common)
        if not os.path.exists(zip_file):
            response = requests.get(down_url)
            if response.status_code == 200:
                with open(zip_file, 'wb') as file:
                    file.write(response.content)
            else:
                print("{} down failed".format(down_url))
        with tarfile.open(zip_file, 'r:gz') as tar:
            tar.extractall(path=zip_file_extrpath)
        print("The {} download successful.".format(down_url))
    if os.path.exists(zip_file_extrpath):
        shutil.copytree(zip_file_extrpath, os.path.join(deb_folder, 'usr/local/lib/python3.10/dist-packages'))

    os.makedirs(os.path.join(deb_folder, 'DEBIAN'), exist_ok = True)
    with open(os.path.join(deb_folder, 'DEBIAN/control'),'w') as f:
        f.write(f'Package: {package_name}\n')
        f.write(f'Version: {version}\n')
        f.write(f'Architecture: arm64\n')
        f.write(f'Maintainer: dianjixz <dianjixz@m5stack.com>\n')
        f.write(f'Original-Maintainer: m5stack <m5stack@m5stack.com>\n')
        f.write(f'Section: llm-module\n')
        f.write(f'Priority: optional\n')
        f.write(f'Homepage: https://www.m5stack.com\n')
        f.write(f'Description: llm-module\n')
        f.write(f' bsp.\n')
    with open(os.path.join(deb_folder, 'DEBIAN/postinst'),'w') as f:
        f.write(f'#!/bin/sh\n')
        f.write(f'[ -f "/lib/systemd/system/llm-sys.service" ] && systemctl enable llm-sys.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-sys.service" ] && systemctl start llm-sys.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-asr.service" ] && systemctl enable llm-asr.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-asr.service" ] && systemctl start llm-asr.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-audio.service" ] && systemctl enable llm-audio.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-audio.service" ] && systemctl start llm-audio.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-kws.service" ] && systemctl enable llm-kws.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-kws.service" ] && systemctl start llm-kws.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-llm.service" ] && systemctl enable llm-llm.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-llm.service" ] && systemctl start llm-llm.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-tts.service" ] && systemctl enable llm-tts.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-tts.service" ] && systemctl start llm-tts.service\n')
        f.write(f'exit 0\n')
    with open(os.path.join(deb_folder, 'DEBIAN/prerm'),'w') as f:
        f.write(f'#!/bin/sh\n')
        f.write(f'[ -f "/lib/systemd/system/llm-tts.service" ] && systemctl stop llm-tts.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-tts.service" ] && systemctl disable llm-tts.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-llm.service" ] && systemctl stop llm-llm.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-llm.service" ] && systemctl disable llm-llm.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-kws.service" ] && systemctl stop llm-kws.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-kws.service" ] && systemctl disable llm-kws.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-audio.service" ] && systemctl stop llm-audio.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-audio.service" ] && systemctl disable llm-audio.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-asr.service" ] && systemctl stop llm-asr.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-asr.service" ] && systemctl disable llm-asr.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-sys.service" ] && systemctl stop llm-sys.service\n')
        f.write(f'[ -f "/lib/systemd/system/llm-sys.service" ] && systemctl disable llm-sys.service\n')
        f.write(f'exit 0\n')
    os.chmod(os.path.join(deb_folder, 'DEBIAN/postinst'), 0o755)
    os.chmod(os.path.join(deb_folder, 'DEBIAN/prerm'), 0o755)
    subprocess.run(["dpkg-deb", "-b", deb_folder, deb_file], check=True)
    print(f"Debian package created: {deb_file}")
    shutil.rmtree(deb_folder)

def create_data_deb(package_name, version, src_folder, revision = 'm5stack1'):
    deb_file = f"{package_name}_{version}-{revision}_arm64.deb"
    deb_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debian')
    if os.path.exists(deb_folder):
        shutil.rmtree(deb_folder)
    os.makedirs(deb_folder, exist_ok = True)

    zip_file = f"m5stack_{package_name}_{version}_data.tar.gz"
    down_url = f"https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/linux/llm/m5stack_{package_name}_{version}_data.tar.gz"
    zip_file_extrpath = f"m5stack_{package_name}_{version}_data"
    if not os.path.exists(zip_file_extrpath):
        # Downloading via HTTP (more common)
        if not os.path.exists(zip_file):
            response = requests.get(down_url)
            if response.status_code == 200:
                with open(zip_file, 'wb') as file:
                    file.write(response.content)
            else:
                print("{} down failed".format(down_url))
        with tarfile.open(zip_file, 'r:gz') as tar:
            tar.extractall(path=zip_file_extrpath)
        print("The {} download successful.".format(down_url))
    if os.path.exists(zip_file_extrpath):
        shutil.copytree(zip_file_extrpath, os.path.join(deb_folder, 'opt/m5stack/data'))

    os.makedirs(os.path.join(deb_folder, 'DEBIAN'), exist_ok = True)
    with open(os.path.join(deb_folder, 'DEBIAN/control'),'w') as f:
        f.write(f'Package: {package_name}\n')
        f.write(f'Version: {version}\n')
        f.write(f'Architecture: arm64\n')
        f.write(f'Maintainer: dianjixz <dianjixz@m5stack.com>\n')
        f.write(f'Original-Maintainer: m5stack <m5stack@m5stack.com>\n')
        f.write(f'Section: llm-module\n')
        f.write(f'Priority: optional\n')
        f.write(f'Homepage: https://www.m5stack.com\n')
        f.write(f'Description: llm-module\n')
        f.write(f' bsp.\n')
    with open(os.path.join(deb_folder, 'DEBIAN/postinst'),'w') as f:
        f.write(f'#!/bin/sh\n')
        f.write(f'exit 0\n')
    with open(os.path.join(deb_folder, 'DEBIAN/prerm'),'w') as f:
        f.write(f'#!/bin/sh\n')
        f.write(f'exit 0\n')
    os.chmod(os.path.join(deb_folder, 'DEBIAN/postinst'), 0o755)
    os.chmod(os.path.join(deb_folder, 'DEBIAN/prerm'), 0o755)
    subprocess.run(["dpkg-deb", "-b", deb_folder, deb_file], check=True)
    print(f"Debian package created: {deb_file}")
    shutil.rmtree(deb_folder)

def create_bin_deb(package_name, version, src_folder, revision = 'm5stack1'):
    deb_file = f"{package_name}_{version}-{revision}_arm64.deb"
    deb_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debian')
    # os.makedirs(deb_folder, exist_ok=True)
    if os.path.exists(deb_folder):
        shutil.rmtree(deb_folder)
    os.makedirs(os.path.join(deb_folder, 'opt/m5stack/bin'), exist_ok = True)
    os.makedirs(os.path.join(deb_folder, 'DEBIAN'), exist_ok = True)
    # shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deb_overlay'), deb_folder)
    shutil.copy2(os.path.join(src_folder, package_name.replace("-", "_")), os.path.join(deb_folder, 'opt/m5stack/bin', package_name.replace("-", "_")))
    with open(os.path.join(deb_folder, 'DEBIAN/control'),'w') as f:
        f.write(f'Package: {package_name}\n')
        f.write(f'Version: {version}\n')
        f.write(f'Architecture: arm64\n')
        f.write(f'Maintainer: dianjixz <dianjixz@m5stack.com>\n')
        f.write(f'Original-Maintainer: m5stack <m5stack@m5stack.com>\n')
        f.write(f'Section: llm-module\n')
        f.write(f'Priority: optional\n')
        f.write(f'Depends: lib-llm\n')
        f.write(f'Homepage: https://www.m5stack.com\n')
        f.write(f'Description: llm-module\n')
        f.write(f' bsp.\n')
    with open(os.path.join(deb_folder, 'DEBIAN/postinst'),'w') as f:
        f.write(f'#!/bin/sh\n')
        f.write(f'[ -f "/lib/systemd/system/{package_name}.service" ] && systemctl enable {package_name}.service\n')
        f.write(f'[ -f "/lib/systemd/system/{package_name}.service" ] && systemctl start {package_name}.service\n')
        f.write(f'exit 0\n')
    with open(os.path.join(deb_folder, 'DEBIAN/prerm'),'w') as f:
        f.write(f'#!/bin/sh\n')
        f.write(f'[ -f "/lib/systemd/system/{package_name}.service" ] && systemctl stop {package_name}.service\n')
        f.write(f'[ -f "/lib/systemd/system/{package_name}.service" ] && systemctl disable {package_name}.service\n')
        f.write(f'exit 0\n')
    os.makedirs(os.path.join(deb_folder, 'lib/systemd/system'), exist_ok = True)
    with open(os.path.join(deb_folder, f'lib/systemd/system/{package_name}.service'),'w') as f:
        f.write(f'[Unit]\n')
        f.write(f'Description={package_name} Service\n')
        if package_name == 'llm-sys':
            f.write(f'After=ubus.service\n')
            f.write(f'Requires=ubus.service\n')
        else:
            f.write(f'After=llm-sys.service\n')
            f.write(f'Requires=llm-sys.service\n')
        f.write(f'\n')
        f.write(f'[Service]\n')
        f.write(f'ExecStart=/opt/m5stack/bin/{package_name.replace("-", "_")}\n')
        f.write(f'WorkingDirectory=/opt/m5stack\n')
        f.write(f'Restart=always\n')
        f.write(f'RestartSec=1\n')
        f.write(f'StartLimitInterval=0\n')
        f.write(f'\n')
        f.write(f'[Install]\n')
        f.write(f'WantedBy=multi-user.target\n')
        f.write(f'\n')

    os.chmod(os.path.join(deb_folder, 'DEBIAN/postinst'), 0o755)
    os.chmod(os.path.join(deb_folder, 'DEBIAN/prerm'), 0o755)
    
    subprocess.run(["dpkg-deb", "-b", deb_folder, deb_file], check=True)
    print(f"Debian package created: {deb_file}")
    shutil.rmtree(deb_folder)

if __name__ == "__main__":

    if "clean" in sys.argv:
        os.system('rm ./*.deb')
        exit(0)
    if "distclean" in sys.argv:
        os.system('rm ./*.deb m5stack_* -rf')
        exit(0)

    version = '1.2'
    data_version = '0.2'
    src_folder = '../dist'
    revision = 'm5stack1'
    create_lib = True
    create_bin = True
    create_data = True
    if len(sys.argv) > 1:
        src_folder = sys.argv[1]
    if (create_lib):
        create_lib_deb('lib-llm', version, src_folder, revision)
    if (create_bin):
        create_bin_deb('llm-sys', version, src_folder, revision)
        create_bin_deb('llm-audio', version, src_folder, revision)
        create_bin_deb('llm-kws', version, src_folder, revision)
        create_bin_deb('llm-asr', version, src_folder, revision)
        create_bin_deb('llm-llm', version, src_folder, revision)
        create_bin_deb('llm-tts', version, src_folder, revision)
        create_bin_deb('llm-melotts', version, src_folder, revision)
    if (create_data):
        create_data_deb('llm-audio-en-us', data_version, src_folder, revision)
        create_data_deb('llm-audio-zh-cn', data_version, src_folder, revision)
        create_data_deb('llm-sherpa-ncnn-streaming-zipformer-20M-2023-02-17', data_version, src_folder, revision)
        create_data_deb('llm-sherpa-ncnn-streaming-zipformer-zh-14M-2023-02-23', data_version, src_folder, revision)
        create_data_deb('llm-sherpa-onnx-kws-zipformer-gigaspeech-3.3M-2024-01-01', data_version, src_folder, revision)
        create_data_deb('llm-sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01', data_version, src_folder, revision)
        # create_data_deb('llm-qwen2-0.5B-prefill-20e', data_version, src_folder, revision)
        # create_data_deb('llm-qwen2-1.5B-prefill-20e', data_version, src_folder, revision)
        create_data_deb('llm-qwen2.5-0.5B-prefill-20e', data_version, src_folder, revision)
        create_data_deb('llm-single-speaker-english-fast', data_version, src_folder, revision)
        create_data_deb('llm-single-speaker-fast', data_version, src_folder, revision)
        create_data_deb('llm-melotts-zh-cn', data_version, src_folder, revision)
