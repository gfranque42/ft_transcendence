Vagrant.configure("2") do |config|
	config.vm.box = "debian/bullseye64"
	config.vm.network "forwarded_port", guest: 8000, host: 8000
	
	config.vm.provider "virtualbox" do |vb|
		vb.memory = 10240
		vb.cpus = 10
	end

	config.vm.provision "shell", inline: <<-SHELL
		export DEBIAN_FRONTEND=noninteractive

		apt-get update
apt-get install -y curl git python3 python3-pip zsh postgresql postgresql-contrib libpq-dev		pip3 install -r /vagrant/requirements.txt

		su -l vagrant -s "/bin/sh" -c "curl -fsSO https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh; chmod 755 install.sh; ./install.sh --unattended"
		chsh -s /bin/zsh vagrant
		echo "cd /vagrant" >> /home/vagrant/.zshrc
		echo 'export PATH=$PATH:/home/vagrant/.local/bin' >> /home/vagrant/.zshrc

		# Add Docker's official GPG key:
		sudo apt-get update
		sudo apt-get install ca-certificates curl
		sudo install -m 0755 -d /etc/apt/keyrings
		sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
		sudo chmod a+r /etc/apt/keyrings/docker.asc

		# Add the repository to Apt sources:
		echo \
		  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
		  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
		  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
		sudo apt-get update

		sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

		# Start and setup PostgreSQL
		service postgresql start
		sudo -u postgres psql -c "CREATE USER username WITH PASSWORD 'password';"
		sudo -u postgres psql -c "ALTER ROLE username SET client_encoding TO 'utf8';"
		sudo -u postgres psql -c "ALTER ROLE username SET default_transaction_isolation TO 'read committed';"
		sudo -u postgres psql -c "ALTER ROLE username SET timezone TO 'UTC';"
		sudo -u postgres psql -c "CREATE DATABASE mydatabase;"
		sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE mydatabase TO username;"

		# Install Django Channels and Daphne explicitly
		pip3 install channels daphne channels_redis

		# django project specific
		sudo docker run -p 6379:6379 -d redis:5
		python3 -c 'import channels; import daphne; print(channels.__version__, daphne.__version__)'
		python3 -m pip install channels_redis

		ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime
		echo "Europe/Paris" > /etc/timezone
		dpkg-reconfigure -f noninteractive tzdata
	SHELL
end
