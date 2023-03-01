# Description
<p>In this project, it is aimed to create an application where staff users can create personnel, update, delete or read personnel they have created. Users without staff feature will be able to read all staff. We also used class-based views to create custom functions and override some methods.👷🏻</p>

# Models

- Personnel
- Department
- User

![Model](https://github.com/klc-pakize/django_person_app/blob/master/PersonnelAppERD.png)

# Department

    - Client_User
        - view department only

    - Staff_User
        - CRUD department

# Personnel

    - Client_User
        - view personnel only

    - Staff_User
        - CRUD personnel (their own personnel)

# Live Project

- <a href="https://pakize.pythonanywhere.com/">Live of the project</a>
- <a href="https://pakize.pythonanywhere.com/swagger/">For the swagger of the project</a>
