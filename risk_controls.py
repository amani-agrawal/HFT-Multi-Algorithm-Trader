import sys

def stop_trading(reason="Unknown"):
    print("\n--------------------Trading Halted--------------------")
    print(f"Reason: {reason}")
    confirm  = input("Should I continue trading (Type 'yes' or 'no')?")
    if confirm=="yes":
        return
    sys.exit(0)
