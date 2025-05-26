import pymysql
import sys
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton,QLabel,QLineEdit,QGridLayout,QVBoxLayout,QMessageBox,QDateEdit,QComboBox,QListWidget
from PyQt6.QtGui import QPalette,QColor
from datetime import date
"Окно Авторизации"
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authorization")
        self.setMinimumSize(QSize(480,700))
        self.setMaximumSize(QSize(690,900))
        self.init_ui()
        self.check_connection()
    
    def check_connection(self):
        try:
            self.connection =  pymysql.connect(
            host='localhost',
            user='kiselevW',
            password='kiselevW',
            database='project_managment_kiselev',
            port=8889
        )
            cursor = self.connection.cursor()
            cursor.execute("Select * From logs where login=0")
            cursor.fetchall()
            self.connection.close()

        except Exception as e:
            QMessageBox.critical(self,"Critical error","No connection database")
            sys.exit(1)


    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        palet = central_widget.palette()
        palet.setColor(QPalette.ColorRole.Window,QColor(237, 230, 214))
        central_widget.setPalette(palet)
        central_widget.setAutoFillBackground(True)

        login_layout = QVBoxLayout()
        """login_layout.addStretch(1)"""
        password_layout = QVBoxLayout()
        """ password_layout.addStretch(1)"""

        layout= QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        self.login_btn = QPushButton("Вход")
        self.login_btn.clicked.connect(self.check_login)
        

        login_lbn = QLabel("Логин")
        self.login_line = QLineEdit()
        login_palet = self.login_line.palette()
        login_palet.setColor(QPalette.ColorRole.Window,QColor(237, 230, 214))
        self.login_line.setPalette(login_palet)
        self.login_line.setAutoFillBackground(True)
        
        login_layout.addWidget(login_lbn,alignment=Qt.AlignmentFlag.AlignCenter)
        login_layout.addWidget(self.login_line)

        password_lbn = QLabel("Пароль")
        self.password_line = QLineEdit()
        self.password_line.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_lbn,alignment=Qt.AlignmentFlag.AlignCenter)
        password_layout.addWidget(self.password_line)


        layout.addWidget(self.login_btn,3,2,1,2,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(login_layout,0,1,1,2,alignment=Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(password_layout,0,3,1,2,alignment=Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignCenter)
        
        central_widget.setLayout(layout)
    
    def check_login(self):
        loging_entry_value = self.login_line.text()
        password_entry_value = self.password_line.text()
        connection = pymysql.connect(
                host='localhost',
                user='kiselevW',
                password='kiselevW',
                database='project_managment_kiselev',
                port=8889         
        )
        self.crs = connection.cursor()
        self.crs.execute("Select * From logs Where login = %s And password = %s",(loging_entry_value,password_entry_value))
        result = self.crs.fetchone()
        connection.close()
        if result:
            self.control_module = ControlModule()
            self.control_module.show()
            self.hide()
        else:
            QMessageBox.warning(self,"NE TOT PASSWORD","I need normally password")
class ControlModule(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление задачами")
        self.resize(1000,1000)
        self.control_init_ui()
        self.db_con()
        self.load_combobox_data()
    
    def db_con(self):
        self.db = pymysql.connect(
            host='localhost',
            user='kiselevW',
            password='kiselevW',
            database='project_managment_kiselev',
            port=8889
        )        
    def control_init_ui(self):
        qwi= QWidget()
        layer = QVBoxLayout()
        palet = qwi.palette()
        palet.setColor(QPalette.ColorRole.Window,QColor(293,188,175))
        qwi.setPalette(palet)
        qwi.setAutoFillBackground(True)
        
        task_box = QGridLayout()
        self.name_task_line = QLineEdit()
        name_lbn = QLabel("Наименование задачи")
        self.deadline_line = QDateEdit()
        self.deadline_line.setDate(date.today())
        deadline_lbn = QLabel("Сроки")
        task_confrim_btn = QPushButton("Подтвердить")
        task_confrim_btn.clicked.connect(self.task_confrim)

        task_box.addWidget(self.name_task_line,0,1)
        task_box.addWidget(name_lbn,0,0)
        task_box.addWidget(self.deadline_line,1,1)
        task_box.addWidget(deadline_lbn,1,0)
        task_box.addWidget(task_confrim_btn,2,0)

        employee_box = QGridLayout()
        self.first_name_line = QLineEdit()
        self.second_name_line = QLineEdit()
        self.specialization_line = QLineEdit()

        first_name_lbn = QLabel("Имя сотрудника")
        second_name_lbn = QLabel("Фамилия")
        specilaziation_lbn = QLabel("Специализация ")

        confrim_employee_btn = QPushButton("Подтвердить")
        confrim_employee_btn.clicked.connect(self.employee_confrim)

        employee_box.addWidget(self.first_name_line,0,1)
        employee_box.addWidget(self.second_name_line,1,1)
        employee_box.addWidget(self.specialization_line,2,1)
        employee_box.addWidget(first_name_lbn,0,0)
        employee_box.addWidget(second_name_lbn,1,0)
        employee_box.addWidget(specilaziation_lbn,2,0)
        employee_box.addWidget(confrim_employee_btn,3,0)

        assigment_box = QGridLayout()
        self.assigment_employee_cmbx = QComboBox()
        self.assigmnet_task_cmbx = QComboBox()
        assigment_employee_lbn = QLabel("Задать сотрудника")
        assigment_task_lbn = QLabel("Задать задачу")
        assigment_confrim_btn = QPushButton("Подтвердить")
        assigment_confrim_btn.clicked.connect(self.assigment_confrim)

        assigment_box.addWidget(self.assigment_employee_cmbx,0,1,1,2)
        assigment_box.addWidget(self.assigmnet_task_cmbx,1,1,1,2)
        assigment_box.addWidget(assigment_task_lbn,1,0)
        assigment_box.addWidget(assigment_employee_lbn,0,0)
        assigment_box.addWidget(assigment_confrim_btn,2,0)

        show_all_btn = QPushButton("Проверить заданные задачи и их ответственных")
        show_all_btn.clicked.connect(self.show_all_confrim)

        layer.addWidget(show_all_btn,stretch=1)
        layer.addLayout(assigment_box)
        layer.addLayout(employee_box)
        layer.addLayout(task_box)
        qwi.setLayout(layer)
        self.setCentralWidget(qwi)
    def task_confrim(self):
        try:
            task_name = self.name_task_line.text()
            deadline = self.deadline_line.date().toString("yyyy-MM-dd")
            
            if not task_name:
                QMessageBox.warning(self, "Внимание", "Не все поля заполнены!")
                return
                
            cursor = self.db.cursor()
            sql = "INSERT INTO task (task_name, task_deadline) VALUES (%s, %s)"
            cursor.execute(sql, (task_name, deadline))
            self.db.commit()
            
            QMessageBox.information(self, "Успех", "Задача добавлена успешно!")
            
        except pymysql.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Ошибка!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
            self.db.rollback()
        finally:
            self.load_combobox_data()
            cursor.close()
    def employee_confrim(self):
        try:
            first_name = self.first_name_line.text()
            second_name = self.second_name_line.text()
            specialization = self.specialization_line.text()
            
            if not all([first_name, second_name, specialization]):
                QMessageBox.warning(self, "Внимание", "Не все поля заполнены!")
                return
                
            cursor = self.db.cursor()
            sql = "INSERT INTO accountable_employee (first_name, second_name, specialization) VALUES (%s, %s, %s)"
            cursor.execute(sql, (first_name, second_name, specialization))
            self.db.commit()
            
            QMessageBox.information(self, "Успех", "Успешно добавили!")
        
        except pymysql.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Такой человек уже существует!")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
            self.db.rollback()
        finally:
            self.load_combobox_data()
            cursor.close()
    def assigment_confrim(self):
        try:
            cursor = self.db.cursor()

            employee_id = self.assigment_employee_cmbx.currentData()
            task_id = self.assigmnet_task_cmbx.currentData()
            
            sql = "INSERT INTO assignment (id_employee, id_task) VALUES (%s, %s)"
            cursor.execute(sql, (employee_id, task_id))
            self.db.commit()
            
            QMessageBox.information(self, "Успех", "Успешно добавлена задача")
    
        except pymysql.IntegrityError as e:
            if "Duplicate entry" in str(e):
                QMessageBox.warning(self, "Ошибка", "Дубликат")
            else:
                QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
            self.db.rollback()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
            self.db.rollback()
        finally:
            self.load_combobox_data()
            cursor.close()
    def show_all_confrim(self):
            self.shfrm = ShowForm()
            self.shfrm.show()

    def load_combobox_data(self):
        self.assigment_employee_cmbx.clear()
        self.assigmnet_task_cmbx.clear()
        cursor = self.db.cursor()
        cursor.execute("SELECT id_employee,first_name, second_name FROM accountable_employee")
        employees = cursor.fetchall()

        for emp in employees:
            self.assigment_employee_cmbx.addItem(f"{emp[1]} {emp[2]}", emp[0])
        
        
        cursor.execute("SELECT id_task_main, task_name FROM task")
        tasks = cursor.fetchall()

        for task in tasks:
            self.assigmnet_task_cmbx.addItem(task[1], task[0])
        cursor.close()
class ShowForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(QSize(720,720))
        self.db = pymysql.connect(
            host='localhost',
            user='kiselevW',
            password='kiselevW',
            database='project_managment_kiselev',
            port=8889
        )
        self.setWindowTitle("Окно просмотра")
        qw = QWidget()
        layout = QVBoxLayout()
        self.qlist = QListWidget(self)

        check_all_btn = QPushButton("Проверить выданные задачи")
        check_all_btn.clicked.connect(self.check_all)
        employee_btn = QPushButton("Список работников")
        employee_btn.clicked.connect(self.check_employee)
        tasks_btn = QPushButton("Проверить задачи")
        tasks_btn.clicked.connect(self.check_task)
        layout.addWidget(tasks_btn)
        layout.addWidget(check_all_btn)
        layout.addWidget(self.qlist)
        layout.addWidget(employee_btn)
        qw.setLayout(layout)

        self.setCentralWidget(qw)

    def check_employee(self):
        self.qlist.clear()
        crs = self.db.cursor()
        sql = "Select * From accountable_employee"
        crs.execute(sql)
        self.qlist.clear()
        for row in crs.fetchall():
            itm_txt = f"----------------------\nИдентификатор сотрудника {row[0]} | Имя {row[1]} | Фамилия {row[2]} | Специализация {row[3]}\n----------------------\n\n"
            self.qlist.addItem(itm_txt)
        crs.close()
    def check_task(self):
        self.qlist.clear()
        crs = self.db.cursor()
        sql = "Select * From task"
        crs.execute(sql)
        self.qlist.clear()
        for row in crs.fetchall():
            itm_txt = f"----------------------\nИдентификатор задачи {row[0]} | Наименование задачи {row[1]} | Сроки {row[2]}\n----------------------\n\n"
            self.qlist.addItem(itm_txt)
        crs.close()
    def check_all(self):
        self.qlist.clear()
        crs = self.db.cursor()
        sql = "Select accountable_employee.id_employee,accountable_employee.first_name,accountable_employee.second_name,accountable_employee.specialization,task.task_name,task.task_deadline,task.id_task_main FROM accountable_employee INNER JOIN assignment ON accountable_employee.id_employee = assignment.id_employee INNER JOIN task on assignment.id_task = task.id_task_main;"
        crs.execute(sql)
        self.qlist.clear()
        for row in crs.fetchall():
            itm_txt = f"----------------------\nНаименование задачи {row[4]}\nИмя ответственного сотрудника {row[1]} | Фамилия {row[2]} | Специализация {row[3]} \nСроки {row[5]} | Идентификатор задачи {row[6]} | Идентификатор сотрудника {row[0]}\n----------------------\n\n"
            self.qlist.addItem(itm_txt)
        crs.close()
        


        



        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    app.exec()
