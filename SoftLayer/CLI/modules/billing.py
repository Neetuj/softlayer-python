"""
usage: sl billing [<command>] [<args>...] [options]

Shows cost incurred to due to created resources.
 
The available commands are:
    list        Lists all ordered resources and their total cost up to this time
    total       Accumulated cost of all resources 
         
e.g.
#Retrieve all iscsi SAN storages ordered and their costing from 2014-03-01(yyyy-mm-dd) to 2014-04-01.
                
sl billing list --from-date 2014-03-01 --to-date 2014-03-01 --group-by "iscsi SAN storage" 
"""
# :license: MIT, see LICENSE for more details.


from datetime import datetime, timedelta
from calendar import monthrange

from SoftLayer.utils import lookup
from SoftLayer.CLI import (
    CLIRunnable, Table, no_going_back, confirm, mb_to_gb, listing,
    FormattedItem)
from SoftLayer.CLI.helpers import (
    CLIAbort, ArgumentError, NestedDict, blank, resolve_id, KeyValueTable,
    update_with_template_args, FALSE_VALUES, export_to_template,
    active_txn, transaction_status)
from SoftLayer import BillingManager


class ListBillingResources(CLIRunnable):
    """
usage: sl billing list [--from-date=date] [--to-date=date] [--group-by=resorce_name]
                       [resource-status=active | inactive]

List resources along with their billing information

Examples:
    sl billing list --from-date=2014-04-01
    sl billing list --to-date=2014-03-01
    sl billing list --group-by=iSCSI SAN Storage
    sl billing list --resource-status=active

Filters:
    -f, --from-date=<date>                  cost incurred from 'from_date'
    -t, --to-date=<date>                    end date to consider, default is latest time stamp.
    -g, --group-by=<resource>               grouping by a resource type e.g cci, server, iscsi etc.
    --resource-status=<active/inactive>     shows only cost of the active(running)/inactive resources

"""
    action = 'list'

    def execute(self, args):
        billing = BillingManager(self.client)
        from_date = None
        to_date = None
        group_by = None
                
        if args.get('--from-date'):
            from_date = args.get('--from-date')
        
        if args.get('--to-date'):
            to_date = args.get('--to-date')
        if args.get('--group-by'):
            group_by = args.get('--group-by')
        #if opt in ('--resource-status'):
        #    kwargs['resource_status'] = arg
        resources = billing.list_resources(from_date, to_date, group_by)

        table = Table(['Order ID', 'Resource Name', 'Resource Type', 'cost', 'create_date'])

        for resource in resources:
            resource = NestedDict(resource)
            table.add_row([
                resource['id'],
                resource['hostName'],
                resource['resourceType'],
                resource['cost'],
                resource['createDate']
            ])                                

        return table
