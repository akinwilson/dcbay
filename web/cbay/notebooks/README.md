## Notes on TESTNET with Electrum 

```
vi +268 ~/.local/share/virtualenvs/very-academy-yt-tutorial-i_x7SZ6d/lib/python3.10/site-packages/electrum/network.py
```
and remove the assert:
```
assert _INSTANCE is None, "Network is a singleton!" 
```
Whilst trying to run on testnet. 



To add coin to a testnet wallet, head to the site:
```
testnet.coinfaucet.eu
```

