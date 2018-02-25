from django.core.exceptions import ValidationError

#n = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

def Validate_studio(value):
    if value[0].isupper():
        return value
    else:
        raise ValidationError("Must huve upper case letter")

    #for x in n:
        #if x in value:
            #raise ValidationError('No ingresar numeros')
        #else:
            #return value
