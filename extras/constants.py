EQUIPMENT_STATUSES = (
    ('installed','Installed'),
    ('checkout','Checkout'),
    ('reserved','Reserved'),
    ('checkedout','Checked out'),
    ('stock','Stock'),
    ('repair','In repair'),
    ('missing','Missing'),
    ('overdue','Overdue'),
    ('missing_paid','Missing, paid for'),
    ('sold','Sold by budget transfer'),
    ('stolen','Stolen'),
    ('surplus','Surplus'),
    ('transferred','Transferred'),
    ('parts','Using for parts'),
)
PRIORITIES = (
    ('1','Urgent'),
    ('2','High'),
    ('3','Medium'),
    ('4','Low'),
    ('5','Lowest'),
)
WORK_TYPES = (
    ('install','Install'),
    ('repair','Repair'),
    ('maintenance','Maintenance'),
    ('replacement','Replacement'),
)
FUNDING_SOURCES = (
    ('dept','Department'),
    ('etc','ETC'),
    ('cpu','CPU'),
    ('bc','Building Construction'),
    ('other','Other'),
    ('mgr','Mountain Grove'),
    ('mc','Media Collections'),
    ('scuf','SCUF'),
)
CHECKOUT_TYPES = (
    ('pickup','Pickup'),
    ('delivery','Delivery'),
)
RETURN_TYPES = (
    ('requestor','Requestor'),
    ('etc','ETC'),
)