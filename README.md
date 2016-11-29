# in-toto demo team ibex

In this demo, we will use in-toto to secure a software supply chain with a very
simple workflow.
Alice will be the project owner - she creates and signs the software supply chain
layout with her private key - and Bob and Carl will be the project functionaries -
they carry out the steps of the software supply chain as defined in the layout.

For the sake of demonstrating in-toto, we will have you run all parts of the
software supply chain.
This is, you will perform the commands on behalf of Alice, Bob and Carl as well
as the client who verifies the final product.


### Download and setup in-toto on *NIX (Linux, OS X, ..)
```shell
# Make sure you have git, python and pip installed on your system
# and get in-toto
git clone -b develop --recursive https://github.com/pkmoore/ibex-toto-demo.git

# Export the envvar required for "simple settings"
export SIMPLE_SETTINGS=toto.settings

### Define software supply chain layout (Alice)
First, we will need to define the software supply chain layout. To simplify this
process, we provide a script that generates a simple layout for the purpose of
the demo. In this software supply chain layout, we have Alice, who is the project
owner that creates the layout, Bob, who creates a Python program
`foo.py`, and Carl, who uses `tar` to package up `foo.py` into a tarball which
together with the in-toto metadata composes the final product that will
eventually be installed and verified by the end user.

```shell
# Create and sign the software supply chain layout on behalf of Alice
cd owner_alice
python create_layout.py
```
The script will create a layout, add Bob's and Carl's public keys (fetched from
their directories), sign it with Alice's private key and dump it to `root.layout`.
In `root.layout`, you will find that (besides the signature and other information)
there are two steps, `after-vcs` and `package`, that the functionaries Steve
and Carl, identified by their public keys, are authorized to perform.

### Write code and push to git using gpg keyring
```shell
cd ../functionary_bob
echo "this is code " >> foo.py

git add foo.py
git commit -m "my commit "
../git-securepush
```
```shell
# Bob has to send the resulting foo.py to Carl so that he can package it
cp foo.py ../functionary_carl/
```


### After VCS (Steve)
Now, we will take the role of the functionary Steve and perform the step
`after-vcs` on his behalf, that is we use in-toto to open an editor and record
metadata for what we do. Execute the following commands to change to Bob's
directory and perform the step.

```shell
cd ../functionary_steve
toto-run.py --step-name after-vcs --products bsl.json --key steve -- python parse_bsl.py
```


### Package (Carl)
Now, we will perform Carl’s `package` step.
Execute the following commands to change to Carl's directory and `tar` up Bob's
`foo.py`:

```shell
cd ../functionary_carl
toto-run.py --step-name package --materials foo.py --products foo.tar.gz --key carl -- tar zcvf foo.tar.gz foo.py
```

This will create another step link metadata file, called `package.link`.
It's time to release our software now.


### Verify final product (client)
Let's first copy all relevant files into the `final_product` that is
our software package `foo.tar.gz` and the related metadata files `root.layout`,
`after-vcs.link` and `package.link`:
```shell
cd ..
cp owner_alice/root.layout functionary_steve/after-vcs.link functionary_steve/bsl.json functionary_carl/package.link functionary_carl/foo.tar.gz final_product/
```
And now run verification on behalf of the client:
```shell
cd final_product
# Fetch Alice's public key from a trusted source to verify the layout signature
# Note: The functionary public keys are fetched from the layout
cd final_product
cp ../owner_alice/alice.pub .
toto-verify.py --layout root.layout --layout-key alice.pub
```
This command will verify that
 1. the layout has not expired,
 2. was signed with Alice’s private key,
<br>and that according to the definitions in the layout
 3. each step was performed and signed by the authorized functionary
 4. the functionaries used the commands they were supposed to use (`vi`,
    `tar`)
 5. the recorded materials and products align with the matchrules and
 6. the inspection `untar` finds what it expects.


From it, you will see the meaningful output `PASSING` and a return value
of `0`, that indicates verification worked out well:
```shell
echo $?
# should output 0
```
