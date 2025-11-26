from datetime import datetime, date
from sqlalchemy import func, and_
from app import db
from apps.expense.models import Expense
from apps.income.models import Income
from apps.saving.models import Saving
from apps.fixed.models import Fixed, FixedHistory


class MonthlyBalanceService:
    """今月の残金計算サービス"""
    
    @staticmethod
    def get_monthly_remaining_balance(user_id, year=None, month=None):
        """
        今月使える残金を計算して返す
        
        Args:
            user_id (int): ユーザーID
            year (int, optional): 年（指定しない場合は今年）
            month (int, optional): 月（指定しない場合は今月）
            
        Returns:
            dict: {
                'remaining_balance': 残金,
                'total_income': 今月の収入合計,
                'total_expense': 今月の支出合計,
                'total_saving': 今月の貯金合計,
                'total_fixed': 今月の固定支出合計,
                'year': 対象年,
                'month': 対象月
            }
        """
        if year is None or month is None:
            today = date.today()
            year = today.year
            month = today.month
        
        # 今月の収入合計
        total_income = MonthlyBalanceService._get_monthly_income(user_id, year, month)
        
        # 今月の支出合計
        total_expense = MonthlyBalanceService._get_monthly_expense(user_id, year, month)
        
        # 今月の貯金合計
        total_saving = MonthlyBalanceService._get_monthly_saving(user_id, year, month)
        
        # 今月の固定支出合計
        total_fixed = MonthlyBalanceService._get_monthly_fixed_expense(user_id, year, month)
        
        # 残金計算：収入 - （支出 + 貯金 + 固定支出）
        remaining_balance = total_income - (total_expense + total_saving + total_fixed)
        
        return {
            'remaining_balance': remaining_balance,
            'total_income': total_income,
            'total_expense': total_expense,
            'total_saving': total_saving,
            'total_fixed': total_fixed,
            'year': year,
            'month': month
        }
    
    @staticmethod
    def _get_monthly_income(user_id, year, month):
        """指定月の収入合計を取得"""
        result = db.session.query(func.sum(Income.amount)).filter(
            and_(
                Income.user_id == user_id,
                func.year(Income.date) == year,
                func.month(Income.date) == month
            )
        ).scalar()
        
        return result or 0
    
    @staticmethod
    def _get_monthly_expense(user_id, year, month):
        """指定月の支出合計を取得"""
        result = db.session.query(func.sum(Expense.amount)).filter(
            and_(
                Expense.user_id == user_id,
                func.year(Expense.date) == year,
                func.month(Expense.date) == month
            )
        ).scalar()
        
        return result or 0
    
    @staticmethod
    def _get_monthly_saving(user_id, year, month):
        """指定月の貯金合計を取得"""
        result = db.session.query(func.sum(Saving.amount)).filter(
            and_(
                Saving.user_id == user_id,
                func.year(Saving.date) == year,
                func.month(Saving.date) == month
            )
        ).scalar()
        
        return result or 0
    
    @staticmethod
    def _get_monthly_fixed_expense(user_id, year, month):
        """指定月の固定支出合計を取得"""
        result = db.session.query(func.sum(FixedHistory.amount)).filter(
            and_(
                FixedHistory.user_id == user_id,
                FixedHistory.year == year,
                FixedHistory.month == month
            )
        ).scalar()
        
        return result or 0
    
    @staticmethod
    def get_daily_average_remaining(user_id, year=None, month=None):
        """
        今月の残り日数で割った1日あたりの使用可能額を計算
        
        Args:
            user_id (int): ユーザーID
            year (int, optional): 年
            month (int, optional): 月
            
        Returns:
            dict: {
                'daily_average': 1日あたりの使用可能額,
                'remaining_days': 今月の残り日数,
                'remaining_balance': 残金
            }
        """
        balance_data = MonthlyBalanceService.get_monthly_remaining_balance(user_id, year, month)
        
        today = date.today()
        if year is None:
            year = today.year
        if month is None:
            month = today.month
        
        # 今月の残り日数を計算
        if year == today.year and month == today.month:
            # 今月の場合、今日から月末までの日数
            if month == 12:
                next_month = date(year + 1, 1, 1)
            else:
                next_month = date(year, month + 1, 1)
            
            remaining_days = (next_month - today).days
        else:
            # 過去・未来の月の場合、その月の日数
            if month == 12:
                next_month = date(year + 1, 1, 1)
            else:
                next_month = date(year, month + 1, 1)
            
            current_month = date(year, month, 1)
            remaining_days = (next_month - current_month).days
        
        # 1日あたりの使用可能額を計算
        daily_average = balance_data['remaining_balance'] / remaining_days if remaining_days > 0 else 0
        
        return {
            'daily_average': daily_average,
            'remaining_days': remaining_days,
            'remaining_balance': balance_data['remaining_balance']
        }