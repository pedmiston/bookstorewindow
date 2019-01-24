# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "geerlingguy/ubuntu1804"
  config.vm.network "forwarded_port", guest: 8000, host: 8001, host_ip: "127.0.0.1"
  config.vm.synced_folder "bookstorewindow", "/apps/bookstorewindow"
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "deploy.yml"
  end
end
