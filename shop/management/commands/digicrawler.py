from rolepermissions.roles import assign_role, clear_roles

from Zibal.models import User
from Zibal.mongoModels import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'migrate'


    def handle(self, *args, **options):
        migrateSubmerchants()
        return None
        #db.pos_transaction.dropIndexes()

        mers = PosMerchant.objects
        for mer in mers:
            Counter(sequence_value = 1383, merchantId = mer.id).save()
        return None
        output = []

        output.append('existing fields changed')

    #assign roles

        users = User.objects.all()
        for user in users:
            clear_roles(user)

            if user.username == "zibaldemo":
                assign_role(user, 'club')
                assign_role(user, 'gateway')
                output.append(user.username+ ' assign club and gateway role')

            if user.status == User.STATUS_ACTIVE:
                assign_role(user, 'pos')
                assign_role(user, 'pos_sandbox')
                output.append(user.username+ ' assign pos and pos_sandbox role')
            elif user.status == User.STATUS_PREACTIVE:
                assign_role(user, 'pos_sandbox')
                output.append(user.username+ ' assign pos_sandbox role')

            if user.is_superuser == 1:
                clear_roles(user)
                assign_role(user, 'admin')
                output.append(user.username+ ' assign admin role')

    #create wallet

        for merchant in PosMerchant.objects:
            wallet = Wallet(credit = merchant.credit,idsql = merchant.idsql, createdAt = merchant.createdAt, minimumCredit = 0, autoCheckout = 0, name = 'اصلی زیبال')
            wallet.save()
            output.append(str(merchant.name)+ ' wallet created')

            merchant.walletId = wallet.id
            merchant.save()

            for log in CreditLog.objects(merchantId = merchant.id).order_by('+createdAt'):
                WalletLog(walletId=wallet.id, createdAt=log.createdAt, amount = log.amount, type = log.type, credit = log.credit, data = log.data).save()

        output.append("done! don't forget to run mongo command and restart socket!!!!!!!!")
        self.stdout.write(self.style.SUCCESS('Successfully done\n'+("\n").join(output)))

#TODO rename transaction to pos_transaction
#TODO rename merchant to pos_merchant
#TODO rename merchant_log_model to api_log
#TODO db.getCollection('pos_merchant').update({}, {$rename:{"Name":"name"}}, false, true);

#TODO rename run migartion

#TODO db.getCollection('gateway_transaction').update({}, {$rename:{"orderId":"trackId"}}, false, true);
#TODO db.getCollection('pos_merchant').update({}, {$unset: {credit:1 }},{multi: true});
#TODO db.pos_transaction.update({"multiplexingInfos.isSelfMerchant": {$exists: true}}, {$unset: {"multiplexingInfos.$.isSelfMerchant":true}}, {multi:true})
#TODO db.getCollection('pos_transaction').update({}, {$rename:{"serialnumber":"terminalId","refnumber":"refNumber","paynumber":"payNumber","cardnumber":"cardNumber"}}, false, true);
#TODO drop credit log and transaction_club

#TODO chenage cron to webhook
#TODO nohup

#TODO don';t forget sandbox change schema

def migrateSubmerchants():

    mers = PosMerchant.objects

    for mer in mers:
        if mer.name!= None:
            SubMerchant(name = mer.name,bankAccount = mer.bankAccount, status = 1,ID='self',idsql = mer.idsql).save()

            for sub in mer.subMerchants:
                try:
                    ss = SubMerchant(name = sub.name,bankAccount = sub.bankAccount, status = sub.status,ID=sub.id,idsql = mer.idsql)
                    if sub.status == 1:
                        ss.isSadad = True
                    ss.save()
                except:
                    print(str(mer.idsql)+" => "+sub.bankAccount)
                    continue