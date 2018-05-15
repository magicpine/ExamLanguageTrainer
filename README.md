# Exam Language Trainer
This is my Final Project for IT Carlow.
Many students take exams that are not written in their mother tongue. This creates problems for students as well as for exam writers. This project will allow quizzes to be automatically generated from electronic format exam papers. The quizzes will be taken via the web by the students prior to the exam taking place. These quizzes could contain unusual words from the exam papers and for example, using MCQs, assess the preparedness of the students to the language they will encounter at exam time without revealing the contents of the exams. This project must be web based.

# To Run this program
You can use any type of cloud solution you want.  The list of the following steps assume that you have already made a server/virtual machine that is using a version of Ubuntu 16.04.4 x64 and you are already logged into it as root.  

1. Add a user named deploy: useradd -r -m -s /bin/bash deploy
2. In order to use python tools you need to use the following commands:
      apt-get install python-setuptools (needed version 2.7 of python)
      easy_install -U pip
3. Install the virtual environment: pip install virtualenv
4. Install git to download the program: apt-get install git
5. Switch to the user you added: su - deploy
6. Clone the repo using this link: https://github.com/magicpine/ExamLanguageTrainer
7. Then enter the directory: cd ExamLanguageTrainer
8. Create a virtual environment and start it up:
      virtualenv venv
      source venv/bin/activate
9. Install the additional files needed by using the requirements file: pip install -r requirements.txt
10. Press ctrl-d to go back into root
11. Install the following additional files, this will allow the server to use special commands to allow files to be converted into a text file:
      Sudo apt-get install openjdk-8-jr
      Sudo apt install poppler-utils
      Sudo apt-get install libreoffice-common
12. Then use sudo apt-get install libreoffice
13. Install Nginx proxy server:
      apt-add-repository ppa:nginx/stable
      apt-get update
      apt-get install nginx
14. Configure the Nginx server to point to gunicorn server and put the following into that file.
      vim /etc/nginx/conf.d/flask-app.conf

          server {
              listen 80;

              server_name _ ;

              access_log  /var/log/nginx/access.log;
              error_log  /var/log/nginx/error.log;

              location / {
                  proxy_pass         http://127.0.0.1:8000/;
                  proxy_redirect     off;

                  proxy_set_header   Host             $host;
                  proxy_set_header   X-Real-IP        $remote_addr;
                  proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
              }
          }

15. Disable the welcome page by:
      vim /etc/nginx/nginx.conf
      Comment out the line using ‘#’: include /etc/nginx/sites-enabled/* ;
16. Change the default settings for network connections:
      vim /etc/nginx/conf.d/timeout.conf

      proxy_connect_timeout       600;
      proxy_send_timeout          600;
      proxy_read_timeout          600;
      send_timeout                600;
17. Reload the changes by: service nginx reload
18. You need to download MongoDB to store information relating to the project. To do so follow this order of steps very carefully.
      sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5
      echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list
      sudo apt-get update
      sudo apt-get install -y mongodb-org
      To allow the server to connect to the mongo program you need to reinstall it by using the following command: sudo apt-get install --reinstall mongodb
19. Log into the user you added: cd deploy
20. Move into the main directory: cd ExamLanguageTrainer
21. Turn on the virtual environment:  source venv/bin/activate
22. Turn on the server using the settings: -t 300 for worker threads lasting 5 minutes and -D for a use of a Daemon server. gunicorn -t 300 -D webapp:app
23. On any web browser use: http://{{IP_OF_SERVER}}
