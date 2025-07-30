#!/usr/bin/env python

sample = """
application.log.2020-03-30-18.prime-ms3-eu-1a-5-433e606f.eu-west-1.amazon.com.gz:Mon Mar 30 18:06:25 2020 UTC MS3 107232-b652b8d1-a39f-4ba1-b8c7-f9695a2a0dc7@prime-ms3-eu-1a-5-433e606f.eu-west-1.amazon.com:0 [WARN] (function-execution-thread-3379) com.amazon.ms3.jsp.util.StringParameterProcessor: RequestId=60555877-a2c3-4848-8f30-46116264e98d CustomerId=AR2GBIR432OHA String william-mobile-slash-prime-migrated-customer-interstitial-header is missing parameter name in template Prime_Mobile_Signup_Offer_Selector_GBB_Monthly_Hero_FT_NL_PrimeMember_Finish_Migration_No_Redirect_Link, owned by ADX
application.log.2020-03-30-18.prime-ms3-eu-1b-2-8c76e785.eu-west-1.amazon.com.gz:Mon Mar 30 18:30:53 2020 UTC MS3 108951-d7708326-3afd-45fe-8cce-77f592684e46@prime-ms3-eu-1b-2-8c76e785.eu-west-1.amazon.com:0 [WARN] (function-execution-thread-836) com.amazon.ms3.jsp.util.StringParameterProcessor: RequestId=J0QAKQAKBZ494J7XKG0K CustomerId=A1B25W24PWLS9K String prime-eink-oobe-main-benefit-details-1-fr is missing parameter kollCount in template WLP_Prime_Signup_OOBE_EinkTablet_PrimeFreeTrial_PAPS_Migration, owned by ADX
application.log.2020-03-30-18.prime-ms3-eu-1b-2-8c76e785.eu-west-1.amazon.com.gz:Mon Mar 30 18:30:53 2020 UTC MS3 108951-d7708326-3afd-45fe-8cce-77f592684e46@prime-ms3-eu-1b-2-8c76e785.eu-west-1.amazon.com:0 [WARN] (function-execution-thread-836) com.amazon.ms3.jsp.util.StringParameterProcessor: RequestId=J0QAKQAKBZ494J7XKG0K CustomerId=A1B25W24PWLS9K String prime-kindle-oobe-ft-legal-text-tnc-popup-fr is missing parameter primeCost in template WLP_Prime_Signup_OOBE_EinkTablet_PrimeFreeTrial_PAPS_Migration, owned by ADX
application.log.2020-03-30-18.prime-ms3-eu-1b-3-d11d9b60.eu-west-1.amazon.com.gz:Mon Mar 30 18:54:24 2020 UTC MS3 100726-7db4f6cc-0774-418c-b52b-abc16abd4a40@prime-ms3-eu-1b-3-d11d9b60.eu-west-1.amazon.com:0 [WARN] (function-execution-thread-903) com.amazon.ms3.jsp.util.StringParameterProcessor: RequestId=1ebd56e8-466c-42d6-9ea2-e450f32ee66d CustomerId=AS3Y4MBE431CK String william-mobile-slash-prime-migrated-customer-interstitial-header is missing parameter name in template Prime_Mobile_Signup_Offer_Selector_GBB_Monthly_Hero_FT_NL_PrimeMember_Finish_Migration_No_Redirect_Link, owned by ADX
"""
#f = open( "log.txt", "w" )
#f.write( sample )

f = open( "log.txt", "r" )
output = f.readlines()
#print output
d = {}
for data in output:
    words = data.split()
    try:
        templateIndex = words.index( "template" ) + 1
        strIndex = words.index( "String" ) + 1
        paramIndex = words.index( "parameter" ) + 1
        template = words[ templateIndex ]
        key = words[ strIndex ] + "        " + words[ paramIndex ]
        if key in d:
            d[ key ].append( template )
        else:
            d[ key ] = [ template ]
    except ValueError:
        pass
for k,v in d.items():
    v = set(v)
    print( k ,  v )
