import enchant

import pronouncing

dictionary = enchant.request_dict("en_US")
print(dictionary.suggest("untrimm'd"))
print(dictionary.suggest("don't"))

phones = pronouncing.phones_for_word("dont")
print(phones)
if phones:
    first_phone = phones[0]
    stresses = pronouncing.stresses(first_phone)
    print(stresses)
