# Expense Splitter Program
# This program helps split expenses equally among friends

def expense_splitter():
    """Main function to calculate and split expenses"""
    
    # Dictionary to store each person's payment
    payments = {}
    
    # Get input from user
    print("=== Expense Splitter ===")
    print("Enter the name and amount paid by each person.")
    print("Type 'done' when finished.\n")
    
    while True:
        name = input("Enter name (or 'done' to finish): ").strip()
        
        if name.lower() == 'done':
            if len(payments) == 0:
                print("Please enter at least one person!")
                continue
            break
        
        try:
            amount = float(input(f"How much did {name} pay? "))
            payments[name] = amount
        except ValueError:
            print("Please enter a valid number!\n")
            continue
    
    # Calculate total amount spent
    total_amount = sum(payments.values())
    
    # Calculate how much each person should pay equally
    num_people = len(payments)
    equal_share = total_amount / num_people
    
    # Calculate balance for each person
    # Positive balance = person overpaid (should receive money)
    # Negative balance = person underpaid (owes money)
    balances = {}
    for name, amount_paid in payments.items():
        balances[name] = amount_paid - equal_share
    
    # Display summary
    print("\n" + "="*40)
    print("EXPENSE SUMMARY")
    print("="*40)
    
    for name, amount in payments.items():
        print(f"{name} paid: ${amount:.2f}")
    
    print(f"\nTotal amount: ${total_amount:.2f}")
    print(f"Equal share per person: ${equal_share:.2f}")
    
    print("\n" + "="*40)
    print("WHO OWES WHOM")
    print("="*40)
    
    # Create lists of people who overpaid and underpaid
    overpaid = {name: balance for name, balance in balances.items() if balance > 0.01}
    underpaid = {name: abs(balance) for name, balance in balances.items() if balance < -0.01}
    
    # Match people who owe money with people who should receive money
    transactions = []
    
    for debtor, debt_amount in underpaid.items():
        remaining_debt = debt_amount
        
        for creditor, credit_amount in list(overpaid.items()):
            if remaining_debt <= 0.01:
                break
            
            if credit_amount > 0.01:
                # Calculate how much to transfer
                transfer_amount = min(remaining_debt, credit_amount)
                
                transactions.append(f"{debtor} owes {creditor} ${transfer_amount:.2f}")
                
                # Update remaining amounts
                remaining_debt -= transfer_amount
                overpaid[creditor] -= transfer_amount
    
    # Print transactions
    if transactions:
        for transaction in transactions:
            print(transaction)
    else:
        print("Everyone paid their fair share! No transfers needed.")
    
    print("="*40)


# Run the program
if __name__ == "__main__":
    expense_splitter()
