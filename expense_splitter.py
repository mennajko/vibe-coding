"""
Expense Splitter Program
------------------------
This program helps split expenses equally among friends by:
1. Collecting payment information from each person
2. Calculating how much each person should pay
3. Determining optimal settlement transactions
4. Saving results to a report file
"""

from datetime import datetime


# ============================================================================
# INPUT FUNCTIONS - Handle user input with validation
# ============================================================================

def get_number_of_friends():
    """
    Get and validate the number of friends participating.
    
    Returns:
        int: Number of friends (minimum 2)
    """
    while True:
        try:
            num_friends = int(input("Enter number of friends: "))
            if num_friends < 2:
                print("❌ Error: You need at least 2 friends to split expenses!")
                continue
            return num_friends
        except ValueError:
            print("❌ Error: Please enter a valid whole number!")


def get_payment_data(num_friends):
    """
    Collect payment information from each friend with validation.
    
    Args:
        num_friends (int): Number of friends to collect data for
        
    Returns:
        dict: Dictionary mapping names to payment amounts
    """
    payments = {}
    
    for i in range(num_friends):
        print()  # Empty line for readability
        
        # Get and validate name
        while True:
            name = input("Enter name: ").strip()
            if not name:
                print("❌ Error: Name cannot be empty!")
                continue
            if name in payments:
                print(f"❌ Error: {name} has already been entered!")
                continue
            break
        
        # Get and validate payment amount
        while True:
            try:
                amount = float(input("Amount paid: ").strip())
                if amount < 0:
                    print("❌ Error: Amount cannot be negative!")
                    continue
                payments[name] = amount
                break
            except ValueError:
                print("❌ Error: Please enter a valid number (e.g., 50 or 50.75)!")
    
    return payments


# ============================================================================
# CALCULATION FUNCTIONS - Process expense data
# ============================================================================

def calculate_balances(payments, equal_share):
    """
    Calculate each person's balance (how much they owe or are owed).
    
    Args:
        payments (dict): Dictionary of name -> amount paid
        equal_share (float): Amount each person should pay
        
    Returns:
        dict: Dictionary of name -> balance
              Positive balance = person is owed money
              Negative balance = person owes money
    """
    balances = {}
    for name, amount_paid in payments.items():
        balances[name] = amount_paid - equal_share
    return balances


def calculate_settlement_transactions(balances):
    """
    Determine optimal transactions to settle all debts.
    
    Uses a greedy algorithm that matches the largest debts with the largest
    credits to minimize the number of transactions needed.
    
    Args:
        balances (dict): Dictionary of name -> balance
        
    Returns:
        list: List of tuples (debtor, creditor, amount)
    """
    # Separate into creditors (owed money) and debtors (owe money)
    creditors = [(name, balance) for name, balance in balances.items() if balance > 0.01]
    debtors = [(name, abs(balance)) for name, balance in balances.items() if balance < -0.01]
    
    # Sort both lists by amount (largest first) for optimal matching
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)
    
    # Convert to mutable lists
    creditors = [[name, amount] for name, amount in creditors]
    debtors = [[name, amount] for name, amount in debtors]
    
    transactions = []
    creditor_idx = 0
    debtor_idx = 0
    
    # Match debtors with creditors using two-pointer approach
    while debtor_idx < len(debtors) and creditor_idx < len(creditors):
        debtor_name, debt_amount = debtors[debtor_idx]
        creditor_name, credit_amount = creditors[creditor_idx]
        
        # Transfer the minimum of what's owed and what's due
        transfer_amount = min(debt_amount, credit_amount)
        transactions.append((debtor_name, creditor_name, transfer_amount))
        
        # Update remaining balances
        debtors[debtor_idx][1] -= transfer_amount
        creditors[creditor_idx][1] -= transfer_amount
        
        # Move to next person if their balance is settled (within 1 cent tolerance)
        if debtors[debtor_idx][1] < 0.01:
            debtor_idx += 1
        if creditors[creditor_idx][1] < 0.01:
            creditor_idx += 1
    
    return transactions


# ============================================================================
# DISPLAY FUNCTIONS - Show results to user
# ============================================================================

def display_expense_summary(payments, total_amount, equal_share, balances, transactions):
    """
    Display complete expense summary to the console.
    
    Args:
        payments (dict): Payment information
        total_amount (float): Total expenses
        equal_share (float): Amount each person should pay
        balances (dict): Individual balances
        transactions (list): Settlement transactions
    """
    # Header
    print("\n" + "="*50)
    print(" "*15 + "EXPENSE SUMMARY")
    print("="*50)
    
    # Payments section
    print("\n📊 PAYMENTS MADE:")
    print("-" * 50)
    for name, amount in payments.items():
        print(f"  {name:<20} paid: ${amount:>8.2f}")
    
    print("\n" + "-" * 50)
    print(f"  {'TOTAL SPENT:':<20}      ${total_amount:>8.2f}")
    print(f"  {'Each person should pay:':<20} ${equal_share:>8.2f}")
    print("-" * 50)
    
    # Balances section
    print("\n💰 BALANCE FOR EACH PERSON:")
    print("-" * 50)
    for name, balance in balances.items():
        if balance > 0.01:
            print(f"  {name:<20} is owed: ${balance:>8.2f}")
        elif balance < -0.01:
            print(f"  {name:<20} owes:    ${abs(balance):>8.2f}")
        else:
            print(f"  {name:<20} is settled ✓")
    print("-" * 50)
    
    # Transactions section
    print("\n🔄 SETTLEMENT TRANSACTIONS:")
    print("-" * 50)
    if transactions:
        for debtor, creditor, amount in transactions:
            print(f"  {debtor} → {creditor}: ${amount:.2f}")
    else:
        print("  ✓ Everyone paid their fair share!")
        print("  No transfers needed.")
    
    print("="*50)
    print(" "*12 + "Settlement Complete!")
    print("="*50)


# ============================================================================
# FILE OPERATIONS - Save and load reports
# ============================================================================

def save_report_to_file(payments, total_amount, equal_share, balances, transactions):
    """
    Save the expense report to a text file.
    
    Args:
        payments (dict): Payment information
        total_amount (float): Total expenses
        equal_share (float): Amount each person should pay
        balances (dict): Individual balances
        transactions (list): Settlement transactions
    """
    try:
        with open("expenses_report.txt", "w", encoding="utf-8") as file:
            # Write header
            file.write("="*50 + "\n")
            file.write(" "*15 + "EXPENSE REPORT\n")
            file.write("="*50 + "\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("="*50 + "\n\n")
            
            # Write payments
            file.write("PAYMENTS MADE:\n")
            file.write("-" * 50 + "\n")
            for name, amount in payments.items():
                file.write(f"  {name:<20} paid: ${amount:>8.2f}\n")
            
            file.write("\n" + "-" * 50 + "\n")
            file.write(f"  {'TOTAL SPENT:':<20}      ${total_amount:>8.2f}\n")
            file.write(f"  {'Each person should pay:':<20} ${equal_share:>8.2f}\n")
            file.write("-" * 50 + "\n\n")
            
            # Write balances
            file.write("BALANCE FOR EACH PERSON:\n")
            file.write("-" * 50 + "\n")
            for name, balance in balances.items():
                if balance > 0.01:
                    file.write(f"  {name:<20} is owed: ${balance:>8.2f}\n")
                elif balance < -0.01:
                    file.write(f"  {name:<20} owes:    ${abs(balance):>8.2f}\n")
                else:
                    file.write(f"  {name:<20} is settled\n")
            file.write("-" * 50 + "\n\n")
            
            # Write transactions
            file.write("SETTLEMENT TRANSACTIONS:\n")
            file.write("-" * 50 + "\n")
            if transactions:
                for debtor, creditor, amount in transactions:
                    file.write(f"  {debtor} -> {creditor}: ${amount:.2f}\n")
            else:
                file.write("  Everyone paid their fair share!\n")
                file.write("  No transfers needed.\n")
            
            file.write("="*50 + "\n")
            file.write(" "*12 + "Settlement Complete!\n")
            file.write("="*50 + "\n")
        
        print(f"\n✅ Report saved to: expenses_report.txt")
    
    except Exception as e:
        print(f"\n⚠️  Warning: Could not save report to file: {e}")


def view_last_result():
    """
    Display the contents of the last saved expense report.
    """
    try:
        with open("expenses_report.txt", "r", encoding="utf-8") as file:
            content = file.read()
            print("\n" + content)
    except FileNotFoundError:
        print("\n❌ No previous report found. Please create an expense split first.")
    except Exception as e:
        print(f"\n❌ Error reading report: {e}")


# ============================================================================
# MAIN WORKFLOW - Orchestrate the expense splitting process
# ============================================================================

def process_new_expense_split():
    """
    Main workflow for processing a new expense split.
    Coordinates all steps from input to output.
    """
    # Step 1: Collect input data
    num_friends = get_number_of_friends()
    payments = get_payment_data(num_friends)
    
    # Step 2: Calculate totals and check for edge cases
    total_amount = sum(payments.values())
    
    if total_amount == 0:
        print("\n⚠️  No expenses to split! Everyone paid $0.00")
        return
    
    # Step 3: Perform calculations
    num_people = len(payments)
    equal_share = total_amount / num_people
    balances = calculate_balances(payments, equal_share)
    transactions = calculate_settlement_transactions(balances)
    
    # Step 4: Display results
    display_expense_summary(payments, total_amount, equal_share, balances, transactions)
    
    # Step 5: Save to file
    save_report_to_file(payments, total_amount, equal_share, balances, transactions)


# ============================================================================
# MENU SYSTEM - User interface
# ============================================================================

def display_menu():
    """
    Display the main menu options.
    """
    print("\n" + "="*50)
    print(" "*12 + "EXPENSE SPLITTER MENU")
    print("="*50)
    print("1. Add new expense split")
    print("2. View last result")
    print("3. Exit")
    print("="*50)


def main():
    """
    Main program loop with menu-driven interface.
    Runs until the user chooses to exit.
    """
    print("\n👋 Welcome to Expense Splitter!")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Process new expense split
            print("\n" + "="*50)
            print(" "*10 + "NEW EXPENSE SPLIT")
            print("="*50)
            try:
                process_new_expense_split()
            except Exception as e:
                print(f"\n❌ Error during expense calculation: {e}")
        
        elif choice == "2":
            # View previous results
            view_last_result()
        
        elif choice == "3":
            # Exit program
            print("\n👋 Thank you for using Expense Splitter. Goodbye!")
            break
        
        else:
            # Invalid input
            print("\n❌ Error: Please enter 1, 2, or 3.")


# ============================================================================
# PROGRAM ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please try again.")
