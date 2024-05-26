#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 18:57:28 2024

@author: guilhermegoncalves
"""

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Clinica Dentária</title>
    {% block title %}
    {% endblock %}
</head>
<body>
    <nav>
        <ul class="menu">
            {% if ulogin == None %}
                <li><a class="button" href="/login">Login</a></li>
            {% else %}
                <li><a class="button" href="/logoff">Logoff</a></li>
                <li><a class="button" href="/gform/Dentist">Dentist</a></li>
                <li><a class="button" href="/submenu?subm=patient">Patient</a></li>
                <li><a class="button" href="/submenu?subm=appointment">Appointment</a></li>
                <li><a class="button" style="color:green">User: {{ulogin}}</a></li>
                <br><br>
                {% if submenu == "patient" %}
                    <li><a class="button" href="/subform/CustomerOrder_OrderProduct?option=''&subm=order">Appointments</a></li>
                    <li><a class="button" href="/order/mapa?option=''">Dentists</a></li>
                {% endif %}
                {% if submenu == "Dentist" %}
                    <li><a class="button" href="/gform/Product?subm=Dentist">Patients</a></li>
                    <li><a class="button" href="/Dentistform?subm=product">Appoitments</a></li>
                {% endif %}
            {% endif %}
        </ul>
        <!-- Adicionar imagem -->
        <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Imagem da Clínica" style="width:300px;height:auto;">
    </nav>
    {% block content %}
    {% endblock %}
    <!-- Adicionar botão de login -->
    <div style="text-align: center;">
        <a class="button" href="/login">Login</a>
    </div>
</body>
</html>