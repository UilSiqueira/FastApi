#Multilingual Content (Portuguese, English)

Instruções de Configuração: Projeto FastAPI com Docker

Este projeto usa Docker para facilitar a configuração e execução do aplicativo FastAPI. Antes de começar, certifique-se de ter o Docker Desktop instalado. Você pode baixá-lo [aqui](https://www.docker.com/products/docker-desktop/).
Você também precisará do Python3.10 ou superior
Observação: Os testes desse projeto foram criados somente com python, sem a utilização de frameworks.
Configuração Inicial

Clone o Repositório:

    git clone https://seurepositorio.git
    cd seu-repositorio

Inicie os Serviços Docker:

    docker-compose up -d --build


Crie as Tabelas do Banco de Dados:

    docker-compose run app sh -c "python db/create_table.py"

Execução dos Testes
    Todos os Testes:
    
    docker-compose run app sh -c "python test/tests_main.py"

Testes Específicos:
Para executar testes específicos, forneça os nomes dos testes como argumentos. Por exemplo, para executar todos os testes que começam com "test_add_product":

    docker-compose run app sh -c "python test/tests_main.py test_add_product"

Subir o Aplicativo:

    docker-compose run app

Observações:
    Certifique-se de que o Docker Desktop está em execução antes de iniciar os serviços Docker.
    Certifique-se de que as permissões necessárias estejam concedidas para execução dos comandos Docker.

Pronto! Seu ambiente FastAPI com Docker está configurado e pronto para ser utilizado. Para mais informações sobre o projeto e suas funcionalidades, consulte a documentação ou o código-fonte do aplicativo.




English

Instructions for Setting Up: FastAPI Project with Docker

This project utilizes Docker to streamline the configuration and execution of the FastAPI application. Before getting started, ensure you have Docker Desktop installed. You can download it here.
You will also need Python 3.10 or later.
Note: The tests in this project were created using only Python, without the use of frameworks.

Initial Setup

  Clone the Repository:

    git clone https://yourrepository.git
    cd your-repository

Start Docker Services:

    docker-compose up -d --build

Create Database Tables:

    docker-compose run app sh -c "python db/create_table.py"

Running Tests

  All Tests:

    docker-compose run app sh -c "python test/tests_main.py"

Specific Tests:
To run specific tests, provide the test names as arguments. For example, to run tests starting with "test_add_product":

bash

    docker-compose run app sh -c "python test/tests_main.py test_add_product"

Run the Application:

    docker-compose run app

Notes

  Ensure Docker Desktop is running before starting Docker services.
  Make sure the necessary permissions are granted for executing Docker commands.

Your FastAPI environment with Docker is now configured and ready to use. For more information about the project and its functionalities, refer to the documentation or the application's source code.

![tests](/Python-API/image/fastapi.png)
