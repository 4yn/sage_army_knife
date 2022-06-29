
sage --preparse sage_army_knife/math.sage
mv sage_army_knife/math.sage.py sage_army_knife/math.py

sage --preparse sage_army_knife/rsa.sage
mv sage_army_knife/rsa.sage.py sage_army_knife/rsa.py

sage --preparse sage_army_knife/lattice.sage
mv sage_army_knife/lattice.sage.py sage_army_knife/lattice.py

sage --preparse sage_army_knife/curve.sage
mv sage_army_knife/curve.sage.py sage_army_knife/curve.py


# download
mkdir -p sage_army_knife/stolen
wget "https://raw.githubusercontent.com/mimoo/RSA-and-LLL-attacks/master/boneh_durfee.sage" -O sage_army_knife/stolen/boneh_durfee.sage.orig -q 2>/dev/null

# apply patch
cp sage_army_knife/stolen/boneh_durfee.sage.orig sage_army_knife/stolen/boneh_durfee.sage
patch sage_army_knife/stolen/boneh_durfee.sage sage_army_knife/stolen/boneh_durfee.sage.patch

# preparse
sage --preparse sage_army_knife/stolen/boneh_durfee.sage
mv sage_army_knife/stolen/boneh_durfee.sage.py sage_army_knife/stolen/boneh_durfee.py


# download
mkdir -p sage_army_knife/stolen
wget "https://raw.githubusercontent.com/defund/coppersmith/master/coppersmith.sage" -O sage_army_knife/stolen/coppersmith.sage.orig -q 2>/dev/null

# apply patch
cp sage_army_knife/stolen/coppersmith.sage.orig sage_army_knife/stolen/coppersmith.sage
patch sage_army_knife/stolen/coppersmith.sage sage_army_knife/stolen/coppersmith.sage.patch

# preparse
sage --preparse sage_army_knife/stolen/coppersmith.sage
mv sage_army_knife/stolen/coppersmith.sage.py sage_army_knife/stolen/coppersmith.py


# download
mkdir -p sage_army_knife/stolen
wget "https://raw.githubusercontent.com/mimoo/Diffie-Hellman_Backdoor/master/backdoor_generator/backdoor_generator.sage" -O sage_army_knife/stolen/dh_backdoor.sage.orig -q 2>/dev/null

# apply patch
cp sage_army_knife/stolen/dh_backdoor.sage.orig sage_army_knife/stolen/dh_backdoor.sage
patch sage_army_knife/stolen/dh_backdoor.sage sage_army_knife/stolen/dh_backdoor.sage.patch

# preparse
sage --preparse sage_army_knife/stolen/dh_backdoor.sage
mv sage_army_knife/stolen/dh_backdoor.sage.py sage_army_knife/stolen/dh_backdoor.py


# download
mkdir -p sage_army_knife/stolen
wget "https://gist.githubusercontent.com/pqlx/d0bdf2d0c4a2aa400b2b52d9bd9b7b65/raw/81c36ec909a56da758c3468132e896bbf128762c/ec-param-check.sage" -O sage_army_knife/stolen/ec_check_param.sage.orig -q 2>/dev/null

# apply patch
cp sage_army_knife/stolen/ec_check_param.sage.orig sage_army_knife/stolen/ec_check_param.sage
patch sage_army_knife/stolen/ec_check_param.sage sage_army_knife/stolen/ec_check_param.sage.patch

# preparse
sage --preparse sage_army_knife/stolen/ec_check_param.sage
mv sage_army_knife/stolen/ec_check_param.sage.py sage_army_knife/stolen/ec_check_param.py

