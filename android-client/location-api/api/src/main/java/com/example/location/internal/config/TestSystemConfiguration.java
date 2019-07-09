package com.example.location.internal.config;

import java.net.Inet4Address;
import java.net.InterfaceAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;
import java.util.List;
import java.util.Optional;

public class TestSystemConfiguration implements SystemConfiguration {

    private String host = "localhost";

    public TestSystemConfiguration() {
        try {
            Enumeration<NetworkInterface> networkInterfaces = NetworkInterface.getNetworkInterfaces();
            while(networkInterfaces.hasMoreElements()) {
                NetworkInterface networkInterface = networkInterfaces.nextElement();
                if(networkInterface.isLoopback()) {
                    continue;
                }
                List<InterfaceAddress> adresses = networkInterface.getInterfaceAddresses();
                Optional<InterfaceAddress> address = adresses.stream().filter(a -> a.getAddress() instanceof Inet4Address).findAny();
                address.ifPresent(interfaceAddress -> host = interfaceAddress.getAddress().getHostName());
                break;
            }
        }catch (Exception e) {
            //do nothing
        }
    }

    @Override
    public String getServerProtocol() {
        return "http";
    }

    @Override
    public String getServerHost() {
        return host;
    }

    @Override
    public int getServerPort() {
        return 5000;
    }
}
