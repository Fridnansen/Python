# -*- coding: utf-8 -*-
import csv
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, Sequence
from sqlalchemy.orm import sessionmaker

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists

from tkinter import *
from tkinter import Tk, Frame, BOTH, LEFT
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased
import sqlite3

Base = declarative_base()


class Course(Base):
    __tablename__ = 'course'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    name = Column(String)

    schoolchildren = relationship('Schoolchild', order_by='Schoolchild.id', back_populates='course')
    course_schedules = relationship('Schedule', order_by='Schedule.time_from', back_populates='course')

    def __repr__(self):
        return "{} {}".format(self.name)


class Schoolchild(Base):
    __tablename__ = 'schoolchild'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    course_id = Column(Integer, ForeignKey('course.id'))

    course = relationship('Course', back_populates='schoolchildren')

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    teacher_schedules = relationship('Schedule', order_by='Schedule.time_from', back_populates='teacher')

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


class Schedule(Base):
    __tablename__ = 'schedule'
    
    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    # Weekday saved as ISO format
    # https://docs.python.org/3/library/datetime.html#datetime.date.isoweekday
    weekday = Column(String)
    time_from = Column(String)
    time_to = Column(String)
    course_id = Column(Integer, ForeignKey('course.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))

    course = relationship('Course', back_populates='course_schedules')
    teacher = relationship('Teacher', back_populates='teacher_schedules')

    def __repr__(self):
        return "{} {}".format(self.name)


class CourseReport(object):

    def __init__(self, path):
        self.path = path

    def export(self, course):
        schoolchildren = course.schoolchildren
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for schoolchild in schoolchildren:
                writer.writerow([str(schoolchild)])


class CourseScheduleReport(object):

    def __init__(self, path):
        self.path = path

    def export(self, course):
        schedules = course.course_schedules
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for schedule in schedules:
                writer.writerow([schedule.weekday, schedule.time_from, schedule.time_to, schedule.teacher])


class TeacherScheduleReport(object):
    
    def __init__(self, path):
        self.path = path

    def export(self, teacher):
        schedules = teacher.teacher_schedules
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for schedule in schedules:
                writer.writerow([schedule.weekday, schedule.time_from, schedule.time_to, schedule.course.name])


"""def main(*args, **kwargs):
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    a_course = Course(name='1A')
    another_course = Course(name='1B')

    a_schoolchild = Schoolchild(firstname='Lucas', lastname='Renx', course=a_course)
    another_schoolchild = Schoolchild(firstname='Pedro', lastname='Gray', course=another_course)
    a_third_schoolchild = Schoolchild(firstname='Maria', lastname='Ferry', course=a_course)

    a_teacher = Teacher(firstname='Jorge', lastname='Manzano')

    a_time = datetime.time(8, 0, 0)
    another_time = datetime.time(10, 0, 0)
    a_third_time = datetime.time(12, 0, 0)

    a_schedule = Schedule(weekday=1, time_from=a_time, time_to=another_time, course=a_course, teacher=a_teacher)
    another_schedule = Schedule(weekday=1, time_from=another_time, time_to=a_third_time,
                                course=another_course, teacher=a_teacher)
    
    session.add(a_course)
    session.add(another_course)

    session.add(a_schoolchild)
    session.add(another_schoolchild)
    session.add(a_third_schoolchild)

    session.add(a_teacher)

    session.add(a_schedule)
    session.add(another_schedule)

    session.commit()

    CourseReport('course_{}.csv'.format(a_course.name)).export(a_course)
    CourseReport('course_{}.csv'.format(another_course.name)).export(another_course)

    CourseScheduleReport('course_schedule_{}.csv'.format(a_course.name)).export(a_course)
    CourseScheduleReport('course_schedule_{}.csv'.format(another_course.name)).export(another_course)

    TeacherScheduleReport('teacher_schedule_{}.csv'.format(a_teacher)).export(a_teacher)


if __name__ == "__main__":
    main()"""


def conexionBBDD():

    miConexion=sqlite3.connect("Curso")
    
    miCursor=miConexion.cursor()


    try:
        miCursor.execute("""CREATE TABLE PROFESOR
            (
            ID_PROFESOR INTEGER,                              
            ID_CURSO INT NOT NULL,                              
            NOMBRES CHAR(50) NOT NULL,                              
            APELLIDOS CHAR(50) NOT NULL,                              
            DNI INT NOT NULL,                              
            DIA CHAR(10) NOT NULL,                              
            INICIO SMALLDATETIME NOT NULL,                              
            FIN SMALLDATETIME NOT NULL,                              
            PRIMARY KEY
                (
                ID_PROFESOR AUTOINCREMENT
                ),
            FOREIGN KEY
                (
                ID_CURSO
                )
                REFERENCES CURSO
                    (
                    ID_CURSO
                    )
            );
        """)

        miCursor.execute("""CREATE TABLE CURSO
            (
            ID_CURSO INTEGER,                              
            CODIGO CHAR(10) NOT NULL,                              
            TITULO VARCHAR(30) NOT NULL,                              
            PRIMARY KEY
                (
                ID_CURSO AUTOINCREMENT
                )
            );
        """)

        miCursor.execute("""CREATE TABLE ALUMNO
            (
            ID_ALUMNO INTEGER,                              
            ID_CURSO INT NOT NULL,                              
            NOMBRES CHAR(50) NOT NULL,                              
            APELLIDOS CHAR(50) NOT NULL,                              
            DNI INT NOT NULL,                              
            PRIMARY KEY
                (
                ID_ALUMNO AUTOINCREMENT
                ),
            FOREIGN KEY
                (
                ID_CURSO
                )
                REFERENCES CURSO
                    (
                    ID_CURSO
                    )
            );
        """)

        
        messagebox.showinfo("BBDD", "BBDD creada con éxito")

    except:

        messagebox.showwarning("¡Atención!", "La BBDD ya existe")

def tabla(query,parameters=()):
    
    with sqlite3.connect("Curso") as miConexion:
    
        miCursor = miConexion.cursor()
        result = miCursor.execute(query, parameters)
        miConexion.commit()

    return result

def seleccionarCurso():

    query = 'SELECT * FROM CURSO ORDER BY ID_CURSO DESC'
    db_rows = tabla(query)
    for row in db_rows:
        impartir=row[2] 
        print(row[2])
    return impartir 

def matriculas1():
    
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    datos= comboxCurso.get()
    Acourse = Course(name=datos)
    
    CourseReport('curso_{}.csv'.format(Acourse.name)).export(Acourse)

    session.commit()
    miConexion.commit()

    messagebox.showinfo("Curso exportado", "Curso {} exportado con éxito".format(Acourse.name))

    """records= cuadro.get_children()
    for element in records:
        cuadro.delete(element)
    query = 'SELECT * FROM ALUMNO ORDER BY ID_ALUMNO DESC'
    db_rows = tabla(query)
    for row in db_rows:
        cuadro.insert('',0, text = row[1], values=row[2])"""

def matriculas2():
    
    records= cuadro.get_children()
    for element in records:
        cuadro.delete(element)
    query = 'SELECT * FROM ALUMNO ORDER BY ID_ALUMNO DESC'
    db_rows = tabla(query)
    for row in db_rows:
        cuadro.insert('',0, text = row[3], values=row[4])

def horarioProfesor1():
    
    records= cuadro.get_children()
    for element in records:
        cuadro.delete(element)
    query = 'SELECT * FROM PROFESOR ORDER BY ID_PROFESOR DESC'
    db_rows = tabla(query)
    for row in db_rows:
        cuadro.insert('',0, text = row[1], values=row[2])

def horarioProfesor2():
    
    records= cuadro.get_children()
    for element in records:
        cuadro.delete(element)
    query = 'SELECT * FROM PROFESOR ORDER BY ID_PROFESOR DESC'
    db_rows = tabla(query)
    for row in db_rows:
        cuadro.insert('',0, text = row[3], values=row[5])

def horarioProfesor3():
    
    records= cuadro.get_children()
    for element in records:
        cuadro.delete(element)
    query = 'SELECT * FROM PROFESOR ORDER BY ID_PROFESOR DESC'
    db_rows = tabla(query)
    for row in db_rows:
        cuadro.insert('',0, text = row[6], values=row[7])

def horarioCurso1():
    
    records= cuadro.get_children()
    for element in records:
        cuadro.delete(element)
    query = 'SELECT * FROM PROFESOR ORDER BY ID_PROFESOR DESC'
    db_rows = tabla(query)
    for row in db_rows:
        cuadro.insert('',0, text = row[1], values=row[5])

def salirAplicacion():

    valor=messagebox.askquestion("Salir", "¿Deseas salir de la aplicación?")

    if valor=="yes":
        root.destroy()

def limpiarCamposProfesor():
    PId.set("")
    PNombre.set("")
    PApellido.set("")
    PDNI.set("")
    comboxCurso.set("Seleccionar:")
    comboxDia.set("Seleccionar:")
    comboxInicio.set("Seleccionar:")
    comboxFin.set("Seleccionar:")

def limpiarCamposAlumno():
    AId.set("")
    ANombre.set("")
    AApellido.set("")
    ADNI.set("")
    comboxCurso.set("")

def limpiarCamposCursos():
    CId.set("")
    Ccodigo.set("")
    comboxCurso.set("")


def crearProfesor():
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    a_teacher = Teacher(firstname=PNombre.get(), lastname=PApellido.get())

    #datos= comboxCurso.get(), PNombre.get(), PApellido.get(), PDNI.get(), comboxDia.get(), comboxInicio.get(), comboxFin.get()
    #miCursor.execute("INSERT INTO PROFESOR VALUES(NULL,?,?,?,?,?,?,?)",(datos))
    
    session.add(a_teacher)

    dia= comboxDia.get()
    a_course = Course(name=dia)

    datos= comboxCurso.get()
    a_course = Course(name=datos)

    inicio= comboxInicio.get()
    #a_time = datetime.time(10, 0, 0)
    
    fin= comboxFin.get()
    #another_time = datetime.time(8, 0, 0)

    a_schedule = Schedule(weekday=dia, time_from=inicio, time_to=fin, course=a_course, teacher=a_teacher)

    session.commit()
    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro insertado con éxito")

def crearAlumno():
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    datos= comboxCurso.get()
    a_course = Course(name=datos)
    a_schoolchild = Schoolchild(firstname= ANombre.get(), lastname= AApellido.get(), course= a_course)

    session.add(a_schoolchild)
    session.add(a_course)
    session.commit()

    miConexion.commit()

    CourseReport('curso_{}.csv'.format(a_course.name)).export(a_course)
    
    messagebox.showinfo("BBDD", "Registro insertado con éxito")


def crearCurso():
    miConexion=sqlite3.connect("Curso")
    miCursor=miConexion.cursor()

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    datos= comboxCurso.get()
    #miCursor.execute("INSERT INTO CURSO VALUES(NULL,?,?)",(datos))
    
    a_course = Course(name=datos)
    session.add(a_course)
    
    session.commit()
    
    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro insertado con éxito")


def leerProfesor():

    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    miCursor.execute("SELECT * FROM PROFESOR WHERE ID_PROFESOR=" + PId.get())
    
    elProfesor=miCursor.fetchall()
    
    for profesor in elProfesor:

        PId.set(profesor[0])
        PNombre.set(profesor[2])
        PApellido.set(profesor[3])
        PDNI.set(profesor[4])
        comboxCurso.set(profesor[1])
        comboxDia.set(profesor[5])
        comboxInicio.set(profesor[6])
        comboxFin.set(profesor[7])

    miConexion.commit()

def leerAlumno():

    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    miCursor.execute("SELECT * FROM ALUMNO WHERE ID_ALUMNO=" + AId.get())
    
    elAlumno=miCursor.fetchall()
    
    for alumno in elAlumno:

        AId.set(alumno[0])
        ANombre.set(alumno[2])
        AApellido.set(alumno[3])
        ADNI.set(alumno[4])
        comboxCurso.set(alumno[1])

    miConexion.commit()


def leerCurso():

    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    #a_course = Course(name=CId.get())
    #miCursor.execute("SELECT * FROM CURSO WHERE ID_CURSO=" + CId.get())
    
    session.select(CId.get())
    elCurso=session.fetchall()
    
    for curso in elCurso:

        CId.set(curso[0])
        Ccodigo.set(curso[1])
        comboxCurso.set(curso[2])

    session.commit()
    miConexion.commit()

def actualizarProfesor():
    
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    datos= comboxCurso.get(), PNombre.get(), PApellido.get(), PDNI.get(), comboxDia.get(), comboxInicio.get(), comboxFin.get()
    miCursor.execute("UPDATE PROFESOR SET ID_CURSO=?, NOMBRES=?, APELLIDOS=?, DNI=?, DIA=?, INICIO=?, FIN=? "+
                        "WHERE ID_PROFESOR=" + PId.get(),(datos))       
        
    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro actualizado con éxito")   


def actualizarAlumno():
    
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    datos= comboxCurso.get(), ANombre.get(), AApellido.get(), ADNI.get()
    miCursor.execute("UPDATE ALUMNO SET ID_CURSO=?, NOMBRES=?, APELLIDOS=?, DNI=?"+
                        "WHERE ID_ALUMNO=" + AId.get(),(datos))     
        
    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro actualizado con éxito")   

def actualizarCurso():
    
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    datos=  comboxCurso.get()
    #miCursor.execute("UPDATE CURSO SET CODIGO=?, TITULO=? "+
                       # "WHERE ID_CURSO=" + CId.get(),(datos))      
    a_course = Course(name=datos) 

    session.update(a_course)

    session.commit()

    miConexion.commit()

    messagebox.showinfo("BBDD", "Registro actualizado con éxito")


def eliminar():
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    miCursor.execute("DELETE FROM DATOUSUARIOS WHERE ID=" + miId.get())

    miConexion.commit()

    messagebox.showinfo ("BBDD", "Registro borrado con éxito")

def eliminarProfesor():
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    miCursor.execute("DELETE FROM PROFESOR WHERE ID_PROFESOR=" + PId.get())

    miConexion.commit()

    messagebox.showinfo ("BBDD", "Registro borrado con éxito")

def eliminarAlumno():
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    miCursor.execute("DELETE FROM ALUMNO WHERE ID_ALUMNO=" + AId.get())

    miConexion.commit()

    messagebox.showinfo ("BBDD", "Registro borrado con éxito")

def eliminarCurso():
    miConexion=sqlite3.connect("Curso")

    miCursor=miConexion.cursor()

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    #miCursor.execute("DELETE FROM CURSO WHERE ID_CURSO=" + CId.get())

    session.delete(CId.get())

    session.commit()
    miConexion.commit()

    messagebox.showinfo ("BBDD", "Registro borrado con éxito")

def acerca():

    messagebox.showinfo ("SISTELAS", "SISTELAS Versión 1.1 \nSistema para Escuelas \nRealizado por: Francisco Díaz")

def onChangeValue(object):
    PDia=comboxDia.get()

def onChangeValue1(object):
    PInicio=comboxInicio.get()

def onChangeValue2(object):
    PFin=comboxFin.get()

def onChangeValue3(object):
    PFin=comboxCurso.get()

root= Tk()

root.title("SISTELAS - Versión 1.1")

#root.iconbitmap("Sis.ico")

root.geometry("1300x600")

notebook=ttk.Notebook(root)
notebook.pack(fill='both', expand='yes')
pes0= ttk.Frame(notebook)
pes1= ttk.Frame(notebook)
pes2= ttk.Frame(notebook)
pes3= ttk.Frame(notebook)
pes4= ttk.Frame(notebook)
notebook.add(pes0, text='Profesor')
notebook.add(pes1, text='Alumno')
notebook.add(pes2, text='Curso')
notebook.add(pes3, text='Matricula')
notebook.add(pes4, text='Horarios')


#----------------------------Menu--------------------------

barraMenu=Menu(root)
root.config(menu=barraMenu, width=300, height=300)

bbddMenu=Menu(barraMenu,tearoff=0)
bbddMenu.add_command(label="Conectar", command= conexionBBDD)
bbddMenu.add_command(label="Salir", command=salirAplicacion)

ayudaMenu=Menu(barraMenu,tearoff=0)
ayudaMenu.add_command(label="Acerca de...", command=acerca)

barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)


#--------------------Comienzo de campos profesor-----------------------

miFrame= Frame(root)
miFrame.pack()

PId=StringVar()
PNombre=StringVar()
PApellido=StringVar()
PDNI=StringVar()
PCursos=StringVar()
PDia=StringVar()
PInicio=StringVar()
PFin=StringVar()
imparte=StringVar()

cuadroID=Entry(pes0, textvariable=PId)
cuadroID.grid(row=1, column=1, padx=10, pady=10)

cuadroNombre=Entry(pes0, textvariable=PNombre)
cuadroNombre.grid(row=2, column=1, padx=10, pady=10)

cuadroApellido=Entry(pes0, textvariable=PApellido)
cuadroApellido.grid(row=3, column=1, padx=10, pady=10)

cuadroDNI=Entry(pes0, textvariable=PDNI)
cuadroDNI.grid(row=4, column=1, padx=10, pady=10)

comboxCurso=Combobox(pes0)
comboxCurso.grid(row=5, column=1, padx=10, pady=10)
items=("Seleccionar:", "Algebra", "Ingles", "Administracion Tributaria","Matematicas", "Python y Base de Datos","Base de Dato", "Programación")
comboxCurso['values']=items
comboxCurso.current(1)
comboxCurso.bind ("<<ComboboxSelected>>", onChangeValue3)

comboxDia=Combobox(pes0)
comboxDia.grid(row=6, column=1, padx=10, pady=10)
items=("Seleccionar:", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo")
comboxDia['values']=items
comboxDia.current(1)
comboxDia.bind ("<<ComboboxSelected>>", onChangeValue)

comboxInicio=Combobox(pes0)
comboxInicio.grid(row=7, column=1, padx=10, pady=10)
items=("Seleccionar:","8:00", "8:45", "9:30", "10:15", "11:00", "11:45", "12:30","13:15", "14:00", "14:45", "15:30", "16:15", "17:00", "17:45", "18:30", "19:15", "20:00")
comboxInicio['values']=items
comboxInicio.current(1)
comboxInicio.bind ("<<ComboboxSelected>>", onChangeValue1)

comboxFin=Combobox(pes0)
comboxFin.grid(row=8, column=1, padx=10, pady=10)
items=("Seleccionar:","8:00", "8:45", "9:30", "10:15", "11:00", "11:45", "12:30","13:15", "14:00", "14:45", "15:30", "16:15", "17:00", "17:45", "18:30", "19:15", "20:00")
comboxFin['values']=items
comboxFin.current(1)
comboxFin.bind ("<<ComboboxSelected>>", onChangeValue2)


#-------------------------label profesor--------------------------

idLabel=Label(pes0,text=" INTRODUZCA PROFESOR ")
idLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)
idLabel.config(fg="blue", justify= "right")

idLabel=Label(pes0, text="ID: ")
idLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

nombreLabel=Label(pes0, text="Nombre: ")
nombreLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

apellidoLabel=Label(pes0, text="Apellido: ")
apellidoLabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

DNILabel=Label(pes0, text="DNI: ")
DNILabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)
    
CursoLabel=Label(pes0, text="Curso a impartir: ")
CursoLabel.grid(row=5, column=0, sticky="e", padx=10, pady=10)

DiaLabel=Label(pes0, text="Dia: ")
DiaLabel.grid(row=6, column=0, sticky="e", padx=10, pady=10)

InicioLabel=Label(pes0, text="Hora de inicio: ")
InicioLabel.grid(row=7, column=0, sticky="e", padx=10, pady=10)

FinLabel=Label(pes0, text="Hora de fin: ")
FinLabel.grid(row=8, column=0, sticky="e", padx=10, pady=10)


#--------------------------- Botones  Profesor---------------------

botonCrear=Button(pes0, text="Crear", command=crearProfesor)
botonCrear.grid(row=10, column=2, sticky="e", padx=10, pady=10)

botonLeer=Button(pes0, text="Exportar Curso",command=matriculas1)
botonLeer.grid(row=10, column=3, sticky="e", padx=10, pady=10)

botonActualizar=Button(pes0, text="Actualizar", command=actualizarProfesor)
botonActualizar.grid(row=10, column=4, sticky="e", padx=10, pady=10)

botonBorrar=Button(pes0, text="Borrar", command=eliminarProfesor)
botonBorrar.grid(row=10, column=5, sticky="e", padx=10, pady=10)

botonlimpiar=Button(pes0, text="Limpiar", command=limpiarCamposProfesor)
botonlimpiar.grid(row=10, column=6, sticky="e", padx=10, pady=10)


#--------------------Comienzo de campos Alumnos-----------------------

AFrame= Frame(root)
AFrame.pack()

AId=StringVar()
ANombre=StringVar()
AApellido=StringVar()
ADNI=StringVar()
ACurso=StringVar()
ADia=StringVar()
AInicio=StringVar()
AFin=StringVar()

AcuadroID=Entry(pes1, textvariable=AId)
AcuadroID.grid(row=1, column=2, padx=10, pady=10)

AcuadroNombre=Entry(pes1, textvariable=ANombre)
AcuadroNombre.grid(row=2, column=2, padx=10, pady=10)

AcuadroApellido=Entry(pes1, textvariable=AApellido)
AcuadroApellido.grid(row=3, column=2, padx=10, pady=10)

AcuadroDNI=Entry(pes1, textvariable=ADNI)
AcuadroDNI.grid(row=4, column=2, padx=10, pady=10)

comboxCurso=Combobox(pes1)
comboxCurso.grid(row=5, column=2, padx=10, pady=10)
items=("Seleccionar:", "Algebra", "Ingles", "Administracion Tributaria","Matematicas", "Python y Base de Datos","Base de Dato", "Programación")
comboxCurso['values']=items
comboxCurso.current(1)
comboxCurso.bind ("<<ComboboxSelected>>", onChangeValue3)


#-------------------------label Alumno--------------------------

ALabel=Label(pes1, text=" INTRODUZCA ALUMNO ")
ALabel.grid(row=0, column=1, sticky="e", padx=10, pady=10)
ALabel.config(fg="red", justify= "right")

ALabel=Label(pes1, text="ID: ")
ALabel.grid(row=1, column=1, sticky="e", padx=10, pady=10)

AnombreLabel=Label(pes1, text="Nombre: ")
AnombreLabel.grid(row=2, column=1, sticky="e", padx=10, pady=10)

AapellidoLabel=Label(pes1, text="Apellido: ")
AapellidoLabel.grid(row=3, column=1, sticky="e", padx=10, pady=10)

ADNILabel=Label(pes1, text="DNI: ")
ADNILabel.grid(row=4, column=1, sticky="e", padx=10, pady=10)

ACursoLabel=Label(pes1, text="Curso a Recibir: ")
ACursoLabel.grid(row=5, column=1, sticky="e", padx=10, pady=10)


#--------------------------- Botones  Alumnos---------------------

botonCrear=Button(pes1, text="Exportar Curso", command=crearAlumno)
botonCrear.grid(row=10, column=2, sticky="e", padx=10, pady=10)

botonLeer=Button(pes1, text="Matriculas",command=matriculas1)
botonLeer.grid(row=10, column=3, sticky="e", padx=10, pady=10)

botonActualizar=Button(pes1, text="Actualizar", command=actualizarAlumno)
botonActualizar.grid(row=10, column=4, sticky="e", padx=10, pady=10)

botonBorrar=Button(pes1, text="Borrar", command=eliminarAlumno)
botonBorrar.grid(row=10, column=5, sticky="e", padx=10, pady=10)

Botonlimpiar=Button(pes1, text="Limpiar", command=limpiarCamposAlumno)
Botonlimpiar.grid(row=10, column=6, sticky="e", padx=10, pady=10)

#--------------------Comienzo de campos Curso-----------------------

miFrame= Frame(root)
miFrame.pack()

CId=StringVar()
Ccodigo=StringVar()
Ccurso=StringVar()

CcuadroID=Entry(pes2, textvariable=CId)
CcuadroID.grid(row=1, column=2, padx=10, pady=10)

CcuadroCodigo=Entry(pes2, textvariable=Ccodigo)
CcuadroCodigo.grid(row=2, column=2, padx=10, pady=10)

comboxCurso=Combobox(pes2)
comboxCurso.grid(row=3, column=2, padx=10, pady=10)
items=("Seleccionar:", "Algebra", "Ingles", "Administracion Tributaria","Matematicas", "Python y Base de Datos","Base de Dato", "Programación")
comboxCurso['values']=items
comboxCurso.current(1)
comboxCurso.bind ("<<ComboboxSelected>>", onChangeValue3)


#-------------------------label curso--------------------------

CLabel=Label(pes2, text=" INTRODUZCA CURSO ")
CLabel.grid(row=0, column=1, sticky="e", padx=10, pady=10)
CLabel.config(fg="green", justify= "right")

IDLabel=Label(pes2, text="ID: ")
IDLabel.grid(row=1, column=1, sticky="e", padx=10, pady=10)

CcodigoLabel=Label(pes2, text="Código: ")
CcodigoLabel.grid(row=2, column=1, sticky="e", padx=10, pady=10)

DescripcionLabel=Label(pes2, text="Titulo: ")
DescripcionLabel.grid(row=3, column=1, sticky="e", padx=10, pady=10)

#--------------------------- Botones Curso ---------------------

botonCrear=Button(pes2, text="Crear", command=crearCurso)
botonCrear.grid(row=4, column=2, sticky="e", padx=10, pady=10)

botonLeer=Button(pes2, text="Leer",command=leerCurso)
botonLeer.grid(row=4, column=3, sticky="e", padx=10, pady=10)

botonActualizar=Button(pes2, text="Actualizar", command=actualizarCurso)
botonActualizar.grid(row=4, column=4, sticky="e", padx=10, pady=10)

botonBorrar=Button(pes2, text="Borrar", command=eliminarCurso)
botonBorrar.grid(row=4, column=5, sticky="e", padx=10, pady=10)

botonlimpiar=Button(pes2, text="Limpiar", command=limpiarCamposCursos)
botonlimpiar.grid(row=4, column=6, sticky="e", padx=10, pady=10)


#------------------------ Label Matricula --------------------------

matriculaLabel=Label(pes3, text="MATRICULA DE ALUMNOS")
matriculaLabel.grid(row=0, column=1, sticky="e", padx=10, pady=10)
matriculaLabel.config(fg="magenta", justify= "center")


#------------------------ campo Matricula--------------------------

cuadro = ttk.Treeview (pes3, height = 10, column =2) 
cuadro.grid(row = 4, column =1, columnspan =2) 
cuadro.heading('#0', text='Curso', anchor=CENTER)
cuadro.heading('#1', text='Nombre', anchor=CENTER)
matriculas2()
cuadro = ttk.Treeview (pes3, height = 10, column =2) 
cuadro.grid(row = 4, column =3, columnspan =2) 
cuadro.heading('#0', text='Apellido', anchor=CENTER)
cuadro.heading('#1', text='DNI', anchor=CENTER)
matriculas2()

#------------------------ Label Horarios --------------------------

matriculaLabel=Label(pes4, text="HORARIO DE PROFESOR")
matriculaLabel.grid(row=0, column=4, sticky="e", padx=10, pady=10)
matriculaLabel.config(fg="Brown", justify= "center")

matriculaLabel=Label(pes4, text="HORARIO DE CURSO")
matriculaLabel.grid(row=5, column=4, sticky="e", padx=10, pady=10)
matriculaLabel.config(fg="Brown", justify= "center")

#------------------------ campo Horarios--------------------------

cuadro = ttk.Treeview (pes4, height = 10, column =2) 
cuadro.grid(row = 4, column =1, columnspan =2) 
cuadro.heading('#0', text='Curso', anchor=CENTER)
cuadro.heading('#1', text='Nombre', anchor=CENTER)
horarioProfesor1()

cuadro = ttk.Treeview (pes4, height = 10, column =2) 
cuadro.grid(row = 4, column =3, columnspan =2) 
cuadro.heading('#0', text='Apellido', anchor=CENTER)
cuadro.heading('#1', text='Dia', anchor=CENTER)
horarioProfesor2()

cuadro = ttk.Treeview (pes4, height = 10, column =2) 
cuadro.grid(row = 4, column =5, columnspan =2) 
cuadro.heading('#0', text='Hora de inicio', anchor=CENTER)
cuadro.heading('#1', text='Hora de fin', anchor=CENTER)
horarioProfesor3()

cuadro = ttk.Treeview (pes4, height = 10, column =2) 
cuadro.grid(row = 8, column =1, columnspan =2) 
cuadro.heading('#0', text='Curso', anchor=CENTER)
cuadro.heading('#1', text='Dia', anchor=CENTER)
horarioCurso1()

cuadro = ttk.Treeview (pes4, height = 10, column =2) 
cuadro.grid(row = 8, column =3, columnspan =2) 
cuadro.heading('#0', text='Hora de Inicio', anchor=CENTER)
cuadro.heading('#1', text='Hora de Fin', anchor=CENTER)
horarioProfesor3()


root.mainloop()