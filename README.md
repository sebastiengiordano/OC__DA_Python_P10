<p align="center">
    <a href="https://user.oc-static.com/upload/2020/09/22/16007803099977_P8%20%281%29.png" class="oc-imageLink oc-imageLink--disabled"><img src="https://user.oc-static.com/upload/2020/09/22/16007803099977_P8%20%281%29.png" alt="Logo"></a>
    <h1 align="center">Soft Desk</h1>
    <h2 align="center">API for report and follow technical problems</h2>
    </br>
    <p align="left">
        This program is the minimum viable product of a back-end used to :
		<ul>
			<li>Create projects</li>
			<li>Add users to these projects (called contributors)</li>
			<li>Create problems within projects</li>
			<li>Create comments linked to a specific problem</li>
		</ul>
    </p>
</p>

<br>
<br>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [How run this program](#how-run-this-program)
  * [Installation](#installation)
  * [Run the program](#run-the-program)

<br>
<br>

<!-- HOW RUN THIS PROGRAM -->
## How run this program

<br>

### Installation

1. Created a folder for this project. Then, open a terminal and go to this folder:
	```sh
	cd "folder project path"
	```
2. Clone the repository:
	```sh
	git clone https://github.com/sebastiengiordano/OC__DA_Python_P10
	```
3. Go to folder OC__DA_Python_P10:
	```sh
	cd OC__DA_Python_P10
	```
4. Create a virtual environment:
	```sh
	python -m venv env
	```
5. Activate the virtual environment:
	```sh
	.\env\Scripts\activate
	```
6. From the "requirements.txt" file, install needed packets:
	```sh
	python -m pip install -r requirements.txt
	```
7. Make database migrations with:
	```sh
	python manage.py makemigrations
	python manage.py migrate
	```

<br>
<br>

### Run the program
1. Open a terminal and go to the folder OC__DA_Python_P10 (if its not already the case):
	```sh
	cd "folder project path" & cd OC__DA_Python_P10
	```
2. Activate the virtual environment (if its not already the case):
	```sh
	.\env\Scripts\activate
	```
3. Run the server:
	```sh
	python manage.py runserver
	```
4. Use the following end-points:
	```sh
	https://documenter.getpostman.com/view/18383749/UVXbuzji
	```
or import the following export (you could find in the root of this API):
	```sh
	Issue Tracking System.postman_collection.json
	```
