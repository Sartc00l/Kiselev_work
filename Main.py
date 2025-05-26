import pymysql
import sys
from PyQt6.QtCore import QSize,Qt
from PyQt6.QtWidgets import QApplication, QWidget,QMainWindow,QPushButton,QLabel,QLineEdit,QGridLayout,QVBoxLayout,QMessageBox,QDateEdit,QComboBox,QListWidget
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
            port=3306
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

        login_layout = QVBoxLayout()
        """login_layout.addStretch(1)"""
        password_layout = QVBoxLayout()
        """ password_layout.addStretch(1)"""

        layout= QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        self.login_btn = QPushButton("Entry")
        self.login_btn.clicked.connect(self.check_login)
        

        login_lbn = QLabel("Login")
        self.login_line = QLineEdit()
        login_layout.addWidget(login_lbn,alignment=Qt.AlignmentFlag.AlignCenter)
        login_layout.addWidget(self.login_line)

        password_lbn = QLabel("Password")
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
                port=3306            
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
        self.setWindowTitle("Task control")
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
            port=3306
        )        
    def control_init_ui(self):
        qwi= QWidget()
        layer = QVBoxLayout()

        
        task_box = QGridLayout()
        self.name_task_line = QLineEdit()
        name_lbn = QLabel("Task name")
        self.deadline_line = QDateEdit()
        self.deadline_line.setDate(date.today())
        deadline_lbn = QLabel("Deadline")
        task_confrim_btn = QPushButton("Confrim")
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

        first_name_lbn = QLabel("First name")
        second_name_lbn = QLabel("Second name")
        specilaziation_lbn = QLabel("Spec ")

        confrim_employee_btn = QPushButton("Confrim")
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
        assigment_employee_lbn = QLabel("Assign employee")
        assigment_task_lbn = QLabel("Assign task")
        assigment_confrim_btn = QPushButton("Confrim")
        assigment_confrim_btn.clicked.connect(self.assigment_confrim)

        assigment_box.addWidget(self.assigment_employee_cmbx,0,1,1,2)
        assigment_box.addWidget(self.assigmnet_task_cmbx,1,1,1,2)
        assigment_box.addWidget(assigment_task_lbn,1,0)
        assigment_box.addWidget(assigment_employee_lbn,0,0)
        assigment_box.addWidget(assigment_confrim_btn,2,0)

        show_all_btn = QPushButton("Check all")
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
                QMessageBox.warning(self, "Warning", "Task name is required!")
                return
                
            cursor = self.db.cursor()
            sql = "INSERT INTO task (task_name, task_deadline) VALUES (%s, %s)"
            cursor.execute(sql, (task_name, deadline))
            self.db.commit()
            
            QMessageBox.information(self, "Success", "Task added successfully!")
            
        except pymysql.IntegrityError:
            QMessageBox.warning(self, "Error", "Task ID already exists!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
            self.db.rollback()
        finally:
            cursor.close()
    def employee_confrim(self):
        try:
            first_name = self.first_name_line.text()
            second_name = self.second_name_line.text()
            specialization = self.specialization_line.text()
            
            if not all([first_name, second_name, specialization]):
                QMessageBox.warning(self, "Warning", "All fields are required!")
                return
                
            cursor = self.db.cursor()
            sql = "INSERT INTO accountable_employee (first_name, second_name, specialization) VALUES (%s, %s, %s)"
            cursor.execute(sql, (first_name, second_name, specialization))
            self.db.commit()
            
            QMessageBox.information(self, "Success", "Employee added successfully!")
        
        except pymysql.IntegrityError:
            QMessageBox.warning(self, "Error", "Employee ID already exists!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
            self.db.rollback()
        finally:
            cursor.close()
    def assigment_confrim(self):
        try:
            cursor = self.db.cursor()

            employee_id = self.assigment_employee_cmbx.currentData()
            task_id = self.assigmnet_task_cmbx.currentData()
            
            sql = "INSERT INTO assignment (id_employee, id_task) VALUES (%s, %s)"
            cursor.execute(sql, (employee_id, task_id))
            self.db.commit()
            
            QMessageBox.information(self, "Success", "Task assigned successfully!")
    
        except pymysql.IntegrityError as e:
            if "Duplicate entry" in str(e):
                QMessageBox.warning(self, "Error", "This assignment already exists or ID is duplicated!")
            else:
                QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
            self.db.rollback()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")
            self.db.rollback()
        finally:
            cursor.close()
    def show_all_confrim(self):
            self.shfrm = ShowForm()
            self.shfrm.show()

    def load_combobox_data(self):
        
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
            port=3306
        )
        qw = QWidget()
        layout = QVBoxLayout()
        self.qlist = QListWidget(self)

        task_btn = QPushButton("check task")
        task_btn.clicked.connect(self.check_task)
        employee_btn = QPushButton("check employee")
        employee_btn.clicked.connect(self.check_employee)

        layout.addWidget(task_btn)
        layout.addWidget(self.qlist)
        layout.addWidget(employee_btn)
        qw.setLayout(layout)

        self.setCentralWidget(qw)

    def check_employee(self):
        crs = self.db.cursor()
        sql = "Select * From accountable_employee"
        crs.execute(sql)
        self.qlist.clear()
        for row in crs.fetchall():
            itm_txt = f"Employee id {row[0]} | First name {row[1]} | Second name {row[2]} | Spec {row[3]}"
            self.qlist.addItem(itm_txt)
        crs.close()
    def check_task(self):
        crs = self.db.cursor()
        sql = "Select * From task"
        crs.execute(sql)
        self.qlist.clear()
        for row in crs.fetchall():
            itm_txt = f"Task id {row[0]} | Task name {row[1]} | task deadline {row[2]}"
            self.qlist.addItem(itm_txt)
        crs.close()


        



        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    app.exec()
