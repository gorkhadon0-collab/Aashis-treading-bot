class RiskManager:
    def __init__(self, max_losses=3, max_daily_trades=20):
        self.max_losses = max_losses
        self.max_daily_trades = max_daily_trades
        self.losses = 0
        self.trades = 0
        self.stopped = False

    def can_trade(self):
        if self.stopped:
            return False
        if self.losses >= self.max_losses:
            self.stopped = True
            return False
        if self.trades >= self.max_daily_trades:
            self.stopped = True
            return False
        return True

    def record_result(self, result):
        if not self.can_trade():
            return

        self.trades += 1

        if result.upper() == "LOSS":
            self.losses += 1

        if self.losses >= self.max_losses:
            self.stopped = True

    def status(self):
        return {
            "trades": self.trades,
            "losses": self.losses,
            "active": self.can_trade()
        }
