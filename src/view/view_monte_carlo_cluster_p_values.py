from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from src.main.config import NUM_DIGITS_ROUND_P_VALUE
from src.view.view_plot import ViewPlot


class ViewMonteCarloClusterPValues(QTableWidget):

    __instance = None

    def __init__(self):
        super().__init__()
        if ViewMonteCarloClusterPValues.__instance is not None:
            raise Exception("ViewMonteCarloClusterPValues should be treated as a singleton class.")
        else:
            ViewMonteCarloClusterPValues.__instance = self

    def init(self):
        self.resize(450, 720)

        self.setColumnCount(2)
        self.setRowCount(len(ModelPlot.get_instance().assoc_rule_p_values))

        self.setWindowTitle(
            "Monte Carlo Simulation (number of trials = " + \
            str(int(ViewPlot.get_instance().num_trials_monte_carlo_input.value())) + \
            ")"
        )
        self.setHorizontalHeaderLabels(["Cluster Association Rule", "P-Value"])

        # adapted from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        assoc_rule_p_values_sorted = sorted(
            ModelPlot.get_instance().assoc_rule_p_values.items(),
            key=lambda item: float(item[1]), # sort by value, which is item[1]
            reverse=False  # so most significant p-values (lowest) show at front of list
        )

        index = 0
        for assoc_rule, p_value in assoc_rule_p_values_sorted:
            assoc_rule_item = QTableWidgetItem(str(assoc_rule))
            assoc_rule_item.setTextAlignment(Qt.AlignRight)
            self.setItem(index, 0, assoc_rule_item)
            rounded_p_value = round(p_value, NUM_DIGITS_ROUND_P_VALUE)
            self.setItem(index, 1, QTableWidgetItem(str(rounded_p_value)))
            index += 1

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewMonteCarloClusterPValues
        """
        if ViewMonteCarloClusterPValues.__instance is not None:
            pass
        else:
            ViewMonteCarloClusterPValues()
        return ViewMonteCarloClusterPValues.__instance

    def show(self) -> None:
        self.init()
        super().show()

from src.model.model_plot import ModelPlot