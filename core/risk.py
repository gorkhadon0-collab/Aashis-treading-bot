import json
import os
from datetime import date
from threading import Lock

STATE_FILE = "data/risk_state.json"


class RiskManager:
    def __init__(self, max_losses=3, max_daily_trades=20):
        self.max_losses = max_losses
        self.max_daily_trades = max_daily_trades
        self.lock = Lock()
        os.makedirs("data", exist_ok=True)
        self.state = self._load()
        self._daily_reset()

    def _default_state(self):
        return {
            "date": str(date.today()),
            "trades": 0,
            "consecutive_losses": 0,
            "total_wins": 0,
            "total_losses": 0,
            "total_draws": 0,
            "stopped": False
        }

    def _load(self):
        try:
            with open(STATE_FILE, "r") as file:
                data = json.load(file)
            default = self._default_state()
            default.update(data)
            return default
        except (OSError, ValueError, TypeError):
            return self._default_state()

    def _save(self):
        temp_file = STATE_FILE + ".tmp"
        with open(temp_file, "w") as file:
            json.dump(self.state, file, indent=2)
        os.replace(temp_file, STATE_FILE)

    def _daily_reset(self):
        today = str(date.today())
        if self.state.get("date") != today:
            self.state["date"] = today
            self.state["trades"] = 0
            self.state["stopped"] = False
            self._save()

    def can_trade(self):
        with self.lock:
            self._daily_reset()

            if self.state["stopped"]:
                return False

            if self.state["consecutive_losses"] >= self.max_losses:
                self.state["stopped"] = True
                self._save()
                return False

            if self.state["trades"] >= self.max_daily_trades:
                self.state["stopped"] = True
                self._save()
                return False

            return True

    def record_result(self, result):
        result = result.upper()

        if result not in ("WIN", "LOSS", "DRAW"):
            raise ValueError("Result must be WIN, LOSS or DRAW")

        with self.lock:
            self._daily_reset()

            if self.state["stopped"]:
                return False

            if self.state["trades"] >= self.max_daily_trades:
                self.state["stopped"] = True
                self._save()
                return False

            self.state["trades"] += 1

            if result == "WIN":
                self.state["total_wins"] += 1
                self.state["consecutive_losses"] = 0

            elif result == "LOSS":
                self.state["total_losses"] += 1
                self.state["consecutive_losses"] += 1

            else:
                self.state["total_draws"] += 1

            if (self.state["consecutive_losses"] >= self.max_losses
                    or self.state["trades"] >= self.max_daily_trades):
                self.state["stopped"] = True

            self._save()
            return True

    def status(self):
        with self.lock:
            self._daily_reset()
            return dict(self.state)

    def emergency_stop(self):
        with self.lock:
            self.state["stopped"] = True
            self._save()
