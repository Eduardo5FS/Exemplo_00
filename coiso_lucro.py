@app.route('/lucro', methods=['GET', 'POST'])
def lucro_diario():
    if request.method == 'POST':
        # Receber dados do formulário de registro
        date = request.form['date']
        lucro_diario=calcular_lucro_diario(date)
        return render_template('lucro.html', lucro_diario=lucro_diario, date=date)
       
        
           
       
    else:
        # Se a solicitação for GET, renderize o template do formulário de registro
        return render_template('lucro.html')
def calcular_lucro_diario(date):
    try:
        conn = sqlite3.connect('clinica.db')
        cur = conn.cursor()

        # Consulta para obter as marcações (consultas) para um determinado dia
        cur.execute('''SELECT motivo FROM Appointment WHERE date = ?''', (date,))
        appointments = cur.fetchall()

        total_lucro = 0

        # Para cada consulta marcada, consultar o preço associado a ela na tabela TypesAppointment e somar ao total
        for appointment in appointments:
            motivo = appointment[0]
            cur.execute('''SELECT preco FROM types_appointment WHERE motivo = ?''', (motivo,))
            preco = cur.fetchone()
            if preco:
                total_lucro += preco[0]  # Adiciona o preço ao total do lucro

        return total_lucro

    except sqlite3.Error as e:
        print("Erro ao calcular lucro diário:", e)
        return 0  # Retorna 0 em caso de erro
    finally:
        conn.close()