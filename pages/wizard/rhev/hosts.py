#allows operations with multiple hosts for RHV Engine and Hypervisor pages
class Hosts():

    def __init__(self, table):
        self.hosts = self._make_host_objects(table)
        self.heads = self._make_heads(table)
        self.table = table

    def _make_host_objects(self, table):
        return [self.Host(tr) for tr in \
            table.find_element_by_tag_name('tbody').\
            find_elements_by_tag_name('tr')]

    def _make_heads(self, table):
        return [head for head in \
            table.find_element_by_tag_name('thead').\
            find_elements_by_tag_name('th')]

    def _get_host_with_attribute(self, attr, is_max):
        dct = {}
        for host in self.hosts:
            dct.update({host:host.get_attr(attr)})
        if is_max:
            return max(dct, key=dct.get)
        else:
            return min(dct, key=dct.get)

    #Methods for choosing single host with minimum or maximum value of an attribute
    def get_host_max_cpu(self):
        return self._get_host_with_attribute('cpu', True)

    def get_host_min_cpu(self):
        return self._get_host_with_attribute('cpu', False)

    def get_host_max_mem(self):
        return self._get_host_with_attribute('memory', True)

    def get_host_min_mem(self):
        return self._get_host_with_attribute('memory', False)

    def get_host_max_disk_space(self):
        return self._get_host_with_attribute('space', True)

    def get_host_min_disk_space(self):
        return self._get_host_with_attribute('space', False)

    #Methods for choosing host by attribute
    #First host that matches the attribute is returned
    def get_host_by_name(self, name):
        sname = str(name)
        for host in self.hosts:
            if host.name() == sname:
                return host
        raise NameError("Could not find host with name '{}'".format(sname))

    def get_host_by_mac(self, mac):
        smac = str(mac)
        for host in self.hosts:
            if host.mac() == smac:
                return host
        raise NameError("Could not find host with mac '{}'".format(smac))

    def get_host_by_type(self, htype):
        shtype = str(htype)
        for host in self.hosts:
            if host.htype() == shtype:
                return host
        raise NameError("Could not find host with type '{}'".format(shtype))

    def get_host_by_cpu(self, cpu):
        icpu = int(cpu)
        for host in self.hosts:
            if host.cpu() == icpu:
                return host
        raise NameError("Could not find host with number of cpus '{}'".format(icpu))

    def get_host_by_memory(self, memory):
        fmemory = float(memory)
        for host in self.hosts:
            if host.memory() == fmemory:
                return host
        raise NameError("Could not find host with memory '{}'".format(fmemory))

    def get_host_by_disks(self, disks):
        idisks = int(disks)
        for host in self.hosts:
            if host.disks() == idisks:
                return host
        raise NameError("Could not find host with number of disks '{}'".format(idisks))

    def get_host_by_space(self, space):
        ispace = int(space)
        for host in self.hosts:
            if host.disk_space() == ispace:
                return host
        raise NameError("Could not find host with disk space '{}'".format(ispace))

    def get_host_by_network(self, network):
        raise NotImplementedError()

    def get_random_host(self):
        import random
        return random.choice(self.hosts)

    def _sort_hosts_by_attribute(self, attr):
        for head in self.heads:
            import string
            text = ''.join(s for s in head.text if s in string.printable)
            if text == attr:
                head.click()

    #Methods for choosing host by the position in the table
    def get_first_host(self):
        new_hosts = self._make_host_objects(self.table)
        return new_hosts[0]

    def get_last_host(self):
        new_hosts = self._make_host_objects(self.table)
        return new_hosts[-1]

    #Methods for sorting hosts in the table by attribute
    def sort_hosts_by_name(self):
        self._sort_hosts_by_attribute("Host Name")

    def sort_hosts_by_mac(self):
        self._sort_hosts_by_attribute("MAC Address")

    def sort_hosts_by_type(self):
        self._sort_hosts_by_attribute("Host Type")

    def sort_hosts_by_cpu(self):
        self._sort_hosts_by_attribute("CPU")

    def sort_hosts_by_memory(self):
        self._sort_hosts_by_attribute("Memory")

    def sort_hosts_by_disks(self):
        self._sort_hosts_by_attribute("# Disks")

    def sort_hosts_by_space(self):
        self._sort_hosts_by_attribute("Disk Space")

    def sort_hosts_by_network(self):
        self._sort_hosts_by_attribute("Network")

    #Represents a single host
    class Host():

        def __init__(self, table_row):
            #data[0] - checkbox
            #data[1] - host name
            #data[2] - MAC address
            #data[3] - host type
            #data[4] - CPU
            #data[5] - memory
            #data[6] - disks
            #data[7] - disk space
            #data[8] - network
            self.data = table_row.find_elements_by_tag_name('td')

        def get_attr(self, attr):
            return {
                'name': self.name(),
                'mac': self.mac(),
                'cpu': self.cpu(),
                'memory': self.memory(),
                'disks': self.disks(),
                'space': self.disk_space(),
                'network': self.network(),
            }.get(attr, None)

        def choose(self):
            self.data[0].click()

        def name(self):
            return str(self.data[1].text)

        def mac(self):
            return str(self.data[2].text)

        def htype(self):
            return str(self.data[3].find_element_by_tag_name('span').\
                get_attribute('data-original-title'))

        def cpu(self):
            return int(filter(str.isdigit, str(self.data[4].text)))

        def memory(self):
            return float(''.join([c for c in self.data[5].text if c in '1234567890.']))

        def disks(self):
            return int(filter(str.isdigit, str(self.data[6].text)))

        def disk_space(self):
            return int(filter(str.isdigit, str(self.data[7].text)))

        def network(self):
            return str(self.data[8].text)

        def set_name(self, name):
            #name can be set only to choosen hypervisor
            self.choose()
            sname = str(name)
            name_field = self.data[1].find_element_by_tag_name('input')
            name_field.clear()
            #this is here because the name field looses focus when hypervisors are sorted
            #sorting is automatic as user writes the name
            for c in sname:
                name_field.send_keys(c)
                name_field.click()

