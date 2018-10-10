# Bounce Classification based on email text

### Sample usage:

```python
with open('sample.txt','r') as f:
	email_text = f.read()
bc = Bounce_classifier(email_text)
# if the email text contains a diagonostic code, use diagonostic_code()
dia_code, classification = bc.diagonostic_code()
# if the email text does not contains a diagonostic code, use no_diagonostic_code()
classification = bc.no_diagonostic_code()
```
