from algopy import ARC4Contract, String, UInt64, Txn, Global, gtxn, itxn, urange
from algopy.arc4 import abimethod, Address, DynamicArray, Struct
# from algopy import ARC4Contract, String
# from algopy.arc4 import abimethod

class Contributor(Struct):
    """Structure to hold contributor information"""
    address: Address
    share_percentage: UInt64  # Percentage (0-100)
    paid: bool  # Track if contributor has been paid

class RantaiAdil(ARC4Contract):
    @abimethod()
    def hello(self, name: String) -> String:
        return "Hello, " + name
    
    """
    A smart contract for splitting payments among multiple contributors.
    
    Features:
    - Project manager can register contributors with their share percentages
    - Client can fund the project
    - Automatic payout distribution when project is marked complete
    """
    
    def __init__(self) -> None:
        """Initialize the contract state"""
        self.manager = Address()  # Project manager address
        self.client = Address()  # Client who will fund the project
        self.total_funded = UInt64(0)  # Total amount funded by client
        self.is_locked = False  # Whether contributor list is locked
        self.is_completed = False  # Whether project is completed
        self.contributors = DynamicArray[Contributor]()  # List of contributors
    
    @abimethod()
    def setup_project(
        self, 
        manager: Address, 
        client: Address
    ) -> String:
        """
        Initialize the project with manager and client addresses.
        Can only be called once.
        
        Args:
            manager: Address of the project manager
            client: Address of the client who will pay
            
        Returns:
            Success message
        """
        # Ensure project hasn't been set up yet
        assert self.manager == Address(), "Project already initialized"
        
        self.manager = manager
        self.client = client
        
        return String("Project setup successful!")
    
    @abimethod()
    def add_contributor(
        self, 
        contributor_address: Address, 
        share_percentage: UInt64
    ) -> String:
        """
        Add a contributor with their share percentage.
        Only manager can call this before locking.
        
        Args:
            contributor_address: Address of the contributor
            share_percentage: Their share (0-100)
            
        Returns:
            Success message
        """
        # Only manager can add contributors
        assert Txn.sender == self.manager, "Only manager can add contributors"
        
        # Cannot add contributors after locking
        assert not self.is_locked, "Contributors list is locked"
        
        # Validate percentage
        assert share_percentage > UInt64(0) and share_percentage <= UInt64(100), "Invalid percentage"
        
        # Create new contributor
        new_contributor = Contributor(
            address=contributor_address,
            share_percentage=share_percentage,
            paid=False
        )

        self.contributors.append(new_contributor.copy())
        
        return String("Contributor added successfully!")
    
    @abimethod()
    def lock_contributors(self) -> String:
        """
        Lock the contributors list to prevent modifications.
        Only manager can call this.
        Validates that total shares equal 100%.
        
        Returns:
            Success message
        """
        # Only manager can lock
        assert Txn.sender == self.manager, "Only manager can lock contributors"
        
        # Cannot lock if already locked
        assert not self.is_locked, "Already locked"
        
        # Must have at least one contributor
        assert self.contributors.length > UInt64(0), "No contributors added"
        
        # Validate that shares sum to 100%
        total_percentage = UInt64(0)
        for i in urange(self.contributors.length):
            total_percentage += self.contributors[i].share_percentage
        
        assert total_percentage == UInt64(100), "Shares must sum to 100%"
        
        self.is_locked = True
        
        return String("Contributors list locked! Ready for funding.")
    
    @abimethod()
    def fund_project(self, payment: gtxn.PaymentTransaction) -> String:
        """
        Client funds the project by sending payment to contract.
        Can only be called after contributors are locked.
        
        Args:
            payment: Payment transaction from client
            
        Returns:
            Success message
        """
        # Only client can fund
        assert Txn.sender == self.client, "Only client can fund"
        
        # Contributors must be locked first
        assert self.is_locked, "Contributors must be locked first"
        
        # Cannot fund if already completed
        assert not self.is_completed, "Project already completed"
        
        # Verify payment goes to contract
        assert payment.receiver == Global.current_application_address, "Payment must go to contract"
        
        # Verify payment amount is reasonable (at least 1 ALGO)
        assert payment.amount >= UInt64(1_000_000), "Minimum funding is 1 ALGO"
        
        self.total_funded += payment.amount
        
        return String("Project funded successfully!")
    
    @abimethod()
    def complete_and_payout(self) -> String:
        """
        Mark project as complete and distribute funds to all contributors.
        Only manager or client can call this.
        
        Returns:
            Success message
        """
        # Only manager or client can complete
        assert Txn.sender == self.manager or Txn.sender == self.client, "Only manager or client can complete"
        
        # Project must be funded
        assert self.total_funded > UInt64(0), "Project not funded yet"
        
        # Cannot complete twice
        assert not self.is_completed, "Project already completed"
        
        # Pay each contributor their share
        for i in urange(self.contributors.length):
            contributor = self.contributors[i].copy()

            if not contributor.paid:
                # Calculate payout amount
                payout_amount = (self.total_funded * contributor.share_percentage) // UInt64(100)

                # Send payment via inner transaction
                itxn.Payment(
                    receiver=contributor.address.native,
                    amount=payout_amount,
                    fee=UInt64(0)  # Contract pays the fee
                ).submit()

                # Mark as paid
                contributor.paid = True
                self.contributors[i] = contributor.copy()
        
        self.is_completed = True
        
        return String("Project completed! All contributors paid.")
    
    @abimethod()
    def get_project_status(self) -> String:
        """
        Get current project status.
        
        Returns:
            Status message
        """
        if not self.is_locked:
            return String("Status: Setting up contributors")
        elif self.total_funded == UInt64(0):
            return String("Status: Waiting for funding")
        elif not self.is_completed:
            return String("Status: Funded, awaiting completion")
        else:
            return String("Status: Completed and paid out")
    
    @abimethod()
    def get_contributor_count(self) -> UInt64:
        """
        Get the number of contributors.
        
        Returns:
            Number of contributors
        """
        return self.contributors.length
