import virtualbox
import vix

import communicator


def main_vix():
    print("opening virtual machine")
    host = vix.VixHost()
    vm = host.open_vm(
        "A:\\Virtual Machines\\windows-10-21h1-x64\\windows-10-21h1-x64.vmx"
    )
    print("powering on")
    vm.power_on()
    print("waiting for tools")
    vm.wait_for_tools()

    instance = communicator.Vix(vm, "vagrant", "vagrant")
    assert instance.connected

    print("uploading file")
    instance.upload("c:\\temp\\test.txt", b"test!")
    print("downloading file")
    assert instance.download("c:\\temp\\test.txt") == b"test!"

    print("running powershell")
    status, stdout, stderr = instance.execute(
        "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "-Command Start-Sleep -s 10",
    )
    assert status == 0
    assert stdout is None
    assert stderr is None


def main_vbox():
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()

    machine = vbox.find_machine("windows-10-2004-x64")
    print(machine.state)
    progress = machine.launch_vm_process(session, "gui", [])
    progress.wait_for_completion()

    print(machine.state)
    instance = communicator.VirtualBox(machine)


if __name__ == "__main__":
    main_vbox()
