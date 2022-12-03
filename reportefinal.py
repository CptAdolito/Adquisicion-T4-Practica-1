import fpdf

#Crear un pdf
pdf = fpdf.FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

#Añadir texto

pdf.cell(200, 10, txt="LOS INGREDIENTES MÁS USADOS EN 2015", ln=1, align="C")

#Guardar la grafica de los ingredientes más usados
pdf.image("graficas/dicc2015.png", x=10, y=10, w=180, h=100)
pdf.ln(100)

pdf.add_page()

pdf.cell(200, 10, txt="INGRESOS POR MES EN 2015", ln=1, align="C")

#Guardar la grafica de los ingresos por mes
pdf.image("graficas/ingre2015.png", x=10, y=10, w=180, h=100)
pdf.ln(100)

pdf.add_page()

pdf.cell(200, 10, txt="LAS PIZZAS MÁS VENDIDAS EN 2015", ln=1, align="C")

#Guardar la grafica de las pizzas más vendidas
pdf.image("graficas/venta2015.png", x=10, y=10, w=180, h=100)
pdf.ln(100)

pdf.add_page()

#Guardar la grafica de los ingredientes más usados
pdf.image("graficas/dicc2016.png", x=10, y=10, w=180, h=100)
pdf.ln(100)
pdf.add_page()
#Guardar la grafica de los ingresos por mes
pdf.image("graficas/ingre2016.png", x=10, y=10, w=180, h=100)
pdf.ln(100)
pdf.add_page()
#Guardar la grafica de las pizzas más vendidas
pdf.image("graficas/venta2016.png", x=10, y=10, w=180, h=100)
pdf.ln(100)


#Guardar el pdf
pdf.output("graficas/graficas15-16.pdf")
