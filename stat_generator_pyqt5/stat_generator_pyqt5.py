import sys, random, time, os
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from pathlib import Path

p = Path(__file__).parent
os.chdir(p)

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        # Main UI code goes here
        self.resize(800, 600)
        self.setWindowTitle("Shinsai's D&D Stat Generator")
        self.statusBar().showMessage(
            "Welcome to Shinsai's D&D Stat Generator!"
        )
        self.main_widget = qtw.QWidget()
        self.setCentralWidget(self.main_widget)
        main_layout = qtw.QHBoxLayout(self.main_widget)
        vert_layout = qtw.QVBoxLayout()
        abilities_layout = qtw.QVBoxLayout()
        main_layout.addLayout(abilities_layout)
        main_layout.addLayout(vert_layout)
        font = qtg.QFont()
        font.setPointSize(25)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction('Show Stat Descriptions', self.show_stat_desc)

        self.priority_label = qtw.QLabel(
            "Drag and drop a stat to adjust it's priority, highest to lowest:"
            ' -Click this text to reset-', self
            )
        self.priority_label.mousePressEvent = self.label_clicked
        self.priority_list = qtw.QListWidget(self)
        self.priority_list.addItems([
                'Strength', 'Dexterity', 'Constitution', "Intelligence",
                'Wisdom', 'Charisma'
        ])
        self.priority_list.setDragDropMode(qtw.QAbstractItemView.InternalMove)
        self.priority_list.setMaximumHeight(110)
        self.priority_list.currentRowChanged.connect(self.update_stats)

        race_label = qtw.QLabel('Select your race (modifiers listed):', self)
        self.race_list = qtw.QComboBox(self)
        self.race_list.addItems([
            "Select your race...", "Dragonborn: Str+2, Cha+1",
            "Half-Elf: Cha+2, two others +1", "Half-Orc: Str+2, Con+1",
            "High Elf: Dex+2, Int+1", "Hill Dwarf: Con+2, Wis+1",
            "Human: Str+1, Dex+1, Con+1, Int+1, Wis+1, Cha+1",
            "Lightfoot Halfling: Dex+2, Cha+1", "Rock Gnome: Int+2, Con+1",
            "Tiefling: Int+1, Cha+2",
        ])
        self.race_list.model().item(0).setEnabled(False)
        self.race_list.currentIndexChanged.connect(self.determine_bonus)
        self.race_list.currentIndexChanged.connect(self.enable_button)
        self.bonuses = {}

        self.main_display = qtw.QTextEdit(
            self, readOnly=True, placeholderText = "Adjust the priority of the"
            " stats in the box above, select your race from the dropdown, then"
            ' press the button below to generate scores.\nPress the "Show Stat'
            ' Descriptions" button in the toolbar to see an overview.'
        )
        self.roll_dem_bones = qtw.QPushButton(
            'Roll to generate your scores', self
        )
        self.roll_dem_bones.setDisabled(True)
        self.roll_dem_bones.clicked.connect(self.get_results)

        vert_layout.addWidget(self.priority_label)
        vert_layout.addWidget(self.priority_list)
        vert_layout.addWidget(race_label)
        vert_layout.addWidget(self.race_list)
        vert_layout.addWidget(self.main_display)
        vert_layout.addWidget(self.roll_dem_bones)

        str_label = qtw.QLabel('Strength', self)
        self.str_box = qtw.QLineEdit(self, readOnly=True, placeholderText='10')
        dex_label = qtw.QLabel('Dexterity', self)
        self.dex_box = qtw.QLineEdit(self, readOnly=True, placeholderText='10')
        con_label = qtw.QLabel('Constitution', self)
        self.con_box = qtw.QLineEdit(self, readOnly=True, placeholderText='10')
        int_label = qtw.QLabel('Intelligence', self)
        self.int_box = qtw.QLineEdit(self, readOnly=True, placeholderText='10')
        wis_label = qtw.QLabel('Wisdom', self)
        self.wis_box = qtw.QLineEdit(self, readOnly=True, placeholderText='10')
        cha_label = qtw.QLabel('Charisma', self)
        self.cha_box = qtw.QLineEdit(self, readOnly=True, placeholderText='10')
        self.str_box.setFixedSize(50, 50)
        self.dex_box.setFixedSize(50, 50)
        self.con_box.setFixedSize(50, 50)
        self.int_box.setFixedSize(50, 50)
        self.wis_box.setFixedSize(50, 50)
        self.cha_box.setFixedSize(50, 50)
        str_label.setAlignment(qtc.Qt.AlignCenter)
        dex_label.setAlignment(qtc.Qt.AlignCenter)
        con_label.setAlignment(qtc.Qt.AlignCenter)
        int_label.setAlignment(qtc.Qt.AlignCenter)
        wis_label.setAlignment(qtc.Qt.AlignCenter)
        cha_label.setAlignment(qtc.Qt.AlignCenter)
        self.str_box.setAlignment(qtc.Qt.AlignCenter)
        self.dex_box.setAlignment(qtc.Qt.AlignCenter)
        self.con_box.setAlignment(qtc.Qt.AlignCenter)
        self.int_box.setAlignment(qtc.Qt.AlignCenter)
        self.wis_box.setAlignment(qtc.Qt.AlignCenter)
        self.cha_box.setAlignment(qtc.Qt.AlignCenter)
        self.str_box.setFont(font)
        self.dex_box.setFont(font)
        self.con_box.setFont(font)
        self.int_box.setFont(font)
        self.wis_box.setFont(font)
        self.cha_box.setFont(font)

        abilities_layout.addWidget(str_label)
        abilities_layout.addWidget(self.str_box)
        abilities_layout.addWidget(dex_label)
        abilities_layout.addWidget(self.dex_box)
        abilities_layout.addWidget(con_label)
        abilities_layout.addWidget(self.con_box)
        abilities_layout.addWidget(int_label)
        abilities_layout.addWidget(self.int_box)
        abilities_layout.addWidget(wis_label)
        abilities_layout.addWidget(self.wis_box)
        abilities_layout.addWidget(cha_label)
        abilities_layout.addWidget(self.cha_box)
        # End main UI code
        self.show()

    @qtc.pyqtSlot(int)
    def update_stats(self):
        """Updates the stats list with new priority order."""
        self.stats = []
        for index in range(self.priority_list.count()):
            self.stats.append(self.priority_list.item(index).text())

    def get_results(self):
        """Rolls the dice, then calculates and prints the results."""
        self.roll_dem_bones.setDisabled(True)
        self.update_stats()
        results = [self.roll_dice(s) for s in (
            'first', 'second', 'third', 'fourth', 'fifth', 'sixth'
        )]
        results.sort(reverse = True)
        time.sleep(.5)
        qtw.qApp.processEvents()
        self.main_display.append(
            f'\nYour results sorted highest to lowest are: {results}\n\n'
            f'Taking into account the {self.race} bonuses, the stats display '
            'to the left has been updated.  Feel free to adjust priorities/'
            'race and roll again.\n'
        )
        stats_dict = {}
        for i,s in enumerate((self.stats)):
            stats_dict[s] = results[i]
        for s in self.bonuses:
            stats_dict[s] = stats_dict[s] + self.bonuses[s]
        self.str_box.setText(f'{stats_dict["Strength"]}')
        self.dex_box.setText(f'{stats_dict["Dexterity"]}')
        self.con_box.setText(f'{stats_dict["Constitution"]}')
        self.int_box.setText(f'{stats_dict["Intelligence"]}')
        self.wis_box.setText(f'{stats_dict["Wisdom"]}')
        self.cha_box.setText(f'{stats_dict["Charisma"]}')
        self.roll_dem_bones.setEnabled(True)

    def show_stat_desc(self):
        """Displays the description screen."""
        qtw.QMessageBox.information(
            self, "Stat Descriptions", '*This list is not comprehensive, and '
            'will vary depending on race/(sub)class.*\n\nStrength\n\t-damage '
            'and attack bonuses for most melee and thrown weapons\n\t-carry '
            'capacity\n\t-Athletics checks\nDexterity\n\t-damage and attack '
            'bonuses for ranged/finesse weapons\n\t-Acrobatics, Stealth, '
            'Sleight of Hand, and Initiative checks\nConstitution\n\t-hit '
            'points\n\t-resistance to poisons, etc.\nIntelligence\n\t-spell '
            'save DC/attack bonus for Wizards\n\t-Arcana, History, '
            'Investigation, Nature, and Religion checks\nWisdom\n\t-spell save'
            ' DC/attack bonus for Druid, Cleric, and Ranger\n\t-Animal '
            'Handling, Insight, Medicine, Perception, and Survival checks\n'
            'Charisma\n\t-spell save DC/attack bonus for Bard, Paladin, '
            'Warlock and Sorceror\n\t-Deception, Intimidation, Performance and'
            ' Persuasion checks'
        )

    def roll_dice(self, ordinal):
        """Roll dem bones."""
        roll = [random.randint(1,6) for x in range(4)]
        roll_sorted = roll[:]
        roll_sorted.sort(reverse=True)
        roll_result = sum(roll_sorted[:3])
        self.main_display.append(
            f'Your {ordinal} roll is: {roll}; dropping the lowest, this '
            f'becomes {roll_sorted[:3]} adding up to {roll_result}.'
        )
        time.sleep(.5)
        qtw.qApp.processEvents()
        return roll_result

    @qtc.pyqtSlot(bool)
    def label_clicked(self, clicked):
        """Reset list order if label is clicked."""
        self.priority_list.clear()
        self.priority_list.addItems([
                'Strength', 'Dexterity', 'Constitution', "Intelligence",
                'Wisdom', 'Charisma'
        ])

    @qtc.pyqtSlot(int)
    def enable_button(self, index):
        """Only enable the roll button if there is a race selected."""
        if index != 0:
            self.roll_dem_bones.setEnabled(True)

    @qtc.pyqtSlot(int)
    def determine_bonus(self, index):
        """Set the bonus based on the selected race."""
        if index == 1:
            self.race = 'Dragonborn'
            self.bonuses = {'Strength': 2, 'Charisma': 1}
        elif index == 2:
            self.race = 'Half-Elf'
            self.bonuses = {'Charisma': 2}
            half_elf_window = HalfElfStatSelection(self)
            half_elf_window.exec()
        elif index == 3:
            self.race = 'Half-Orc'
            self.bonuses = {'Strength': 2, 'Constitution': 1}
        elif index == 4:
            self.race = 'High Elf'
            self.bonuses = {'Dexterity': 2, 'Intelligence': 1}
        elif index == 5:
            self.race = 'Hill Dwarf'
            self.bonuses = {'Constitution': 2, 'Intelligence': 1}
        elif index == 6:
            self.race = 'Human'
            self.bonuses = {
                'Strength': 1, 'Dexterity': 1, 'Constitution': 1,
                'Intelligence': 1, 'Wisdom': 1, 'Charisma': 1
            }
        elif index == 7:
            self.race = 'Lightfoot Halfling'
            self.bonuses = {'Dexterity': 2, 'Charisma': 1}
        elif index == 8:
            self.race = 'Rock Gnome'
            self.bonuses = {'Intelligence': 2, 'Constitution': 1}
        elif index == 9:
            self.race = 'Tiefling'
            self.bonuses = {'Intelligence': 1, 'Charisma': 2}


class HalfElfStatSelection(qtw.QDialog):
    """Prompt user to select stats for a Half-Elf."""
    def __init__(self, parent=None):
        """Set up the window UI."""
        super().__init__(parent, modal=True)
        self.setWindowTitle("Half-Elf Stat Selection")
        self.resize(400, 100)
        layout = qtw.QGridLayout()
        self.setLayout(layout)
        label = qtw.QLabel('Select 2 abilities to improve by +1:')
        label.setAlignment(qtc.Qt.AlignCenter)
        layout.addWidget(label, 0, 0, 1, 3)
        self.num_checked = 0
        self.str_checkbox = qtw.QCheckBox('Strength')
        self.dex_checkbox = qtw.QCheckBox('Dexterity')
        self.con_checkbox = qtw.QCheckBox('Constitution')
        self.int_checkbox = qtw.QCheckBox('Intelligence')
        self.wis_checkbox = qtw.QCheckBox('Wisdom')
        self.checkboxes = [
            self.str_checkbox, self.dex_checkbox, self.con_checkbox,
            self.int_checkbox, self.wis_checkbox
        ]
        for checkbox in self.checkboxes:
            checkbox.toggled.connect(self.adjust_nums_checked)

        layout.addWidget(self.str_checkbox, 1, 0)
        layout.addWidget(self.dex_checkbox, 1, 1)
        layout.addWidget(self.con_checkbox, 1, 2)
        layout.addWidget(self.int_checkbox, 2, 0)
        layout.addWidget(self.wis_checkbox, 2, 1)
        reset_checkboxes = qtw.QPushButton('Clear', self)
        self.submit_btn = qtw.QPushButton('Ok', self, clicked=self.accept)
        self.submit_btn.setDisabled(True)
        layout.addWidget(reset_checkboxes, 3, 1)
        layout.addWidget(self.submit_btn, 3, 2)
        reset_checkboxes.clicked.connect(self.remove_checks)

    @qtc.pyqtSlot(bool)
    def adjust_nums_checked(self, checked):
        """Keep track of number of abilities checked; act according."""
        mw.checked_stats = []
        if checked:
            self.num_checked += 1
        elif not checked:
            self.num_checked -= 1
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                mw.checked_stats.append(checkbox)
                mw.bonuses[checkbox.text()] = 1
        for checkbox in self.checkboxes:
            if self.num_checked == 2:
                if not checkbox.isChecked():
                    checkbox.setDisabled(True)
                    if checkbox.text() in mw.bonuses.keys():
                        del mw.bonuses[checkbox.text()]
                self.submit_btn.setEnabled(True)
            else:
                checkbox.setDisabled(False)
                self.submit_btn.setEnabled(False)

    @qtc.pyqtSlot()
    def remove_checks(self):
        """Clears any checked boxes."""
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
        mw.checked_stats = []
        mw.bonuses = {'Charisma': 2}

    def accept(self):
        """Accepts the input."""
        super().accept()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon('dice.ico'))
    mw = MainWindow()
    sys.exit(app.exec())