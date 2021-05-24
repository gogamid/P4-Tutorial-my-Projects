from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import SimpleSwitchAPI
from scapy.all import sniff

MIRROR_SESSION_ID = 99


class LearningSwitchControllerApp(object):

    def __init__(self, switchName):
        self.topo = Topology(db="topology.db") #???
        self.switchName = switchName
        self.thrift_port = self.topo.get_thrift_port(switchName)
        self.cpu_port = self.topo.get_cpu_port_index(self.switchName)
        self.controller = SimpleSwitchAPI(self.thrift_port)

        self.init()

    def init(self):
        self.controller.reset_state()
        self.add_mirror()

    def add_mirror(self):
        if self.cpu_port:
            self.controller.mirroring_add(MIRROR_SESSION_ID, self.cpu_port)

  
    def recv_msg_cpu(self, pkt):

        self.controller.register_write("MyIngress.dropRates", 3, 14)

    def run_cpu_port_loop(self):

        cpu_port_intf = str(self.topo.get_cpu_port_intf(
            self.switchName).replace("eth0", "eth1"))
        sniff(iface=cpu_port_intf, prn=self.recv_msg_cpu)


if __name__ == "__main__":
    import sys
    switchName = sys.argv[1]
    controller = LearningSwitchControllerApp(switchName).run_cpu_port_loop()
