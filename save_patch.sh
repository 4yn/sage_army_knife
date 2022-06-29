#!/usr/bin/env bash

# download
mkdir -p sage_army_knife/stolen
wget "https://raw.githubusercontent.com/defund/coppersmith/master/coppersmith.sage" -O sage_army_knife/stolen/coppersmith.sage.orig -q 2>/dev/null

# save patch
diff sage_army_knife/stolen/coppersmith.sage.orig sage_army_knife/stolen/coppersmith.sage > sage_army_knife/stolen/coppersmith.sage.patch


# download
mkdir -p sage_army_knife/stolen
wget "https://raw.githubusercontent.com/mimoo/Diffie-Hellman_Backdoor/master/backdoor_generator/backdoor_generator.sage" -O sage_army_knife/stolen/dh_backdoor.sage.orig -q 2>/dev/null

# # save patch
diff sage_army_knife/stolen/dh_backdoor.sage.orig sage_army_knife/stolen/dh_backdoor.sage > sage_army_knife/stolen/dh_backdoor.sage.patch


# download
mkdir -p sage_army_knife/stolen
wget "https://raw.githubusercontent.com/mimoo/RSA-and-LLL-attacks/master/boneh_durfee.sage" -O sage_army_knife/stolen/boneh_durfee.sage.orig -q 2>/dev/null

# save patch
diff sage_army_knife/stolen/boneh_durfee.sage.orig sage_army_knife/stolen/boneh_durfee.sage > sage_army_knife/stolen/boneh_durfee.sage.patch


# download
mkdir -p sage_army_knife/stolen
wget "https://gist.githubusercontent.com/pqlx/d0bdf2d0c4a2aa400b2b52d9bd9b7b65/raw/81c36ec909a56da758c3468132e896bbf128762c/ec-param-check.sage" -O sage_army_knife/stolen/ec_check_param.sage.orig -q 2>/dev/null

# # save patch
diff sage_army_knife/stolen/ec_check_param.sage.orig sage_army_knife/stolen/ec_check_param.sage > sage_army_knife/stolen/ec_check_param.sage.patch
