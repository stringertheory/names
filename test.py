import enchant

import pronouncing

dictionary = enchant.request_dict("en_US")
print dictionary.suggest("untrimm'd")

phones = pronouncing.phones_for_word("untrimmed")
if phones:
    first_phone = phones[0]
    stresses = pronouncing.stresses(first_phone)
    print stresses
