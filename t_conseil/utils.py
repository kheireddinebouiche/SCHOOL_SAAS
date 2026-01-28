def num_to_words_fr(number):
    """
    Converts a number to French words with "Dinars Algériens" and "Centimes".
    Suitable for DZA currency.
    """
    units = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
    teens = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
    tens = ["", "dix", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingts", "quatre-vingt-dix"]

    def convert_group(n):
        if n == 0:
            return ""
        res = ""
        h = n // 100
        t = (n % 100) // 10
        u = n % 10

        if h > 0:
            if h == 1:
                res += "cent "
            else:
                res += units[h] + " cent "
        
        if t == 1:
            res += teens[u]
        elif t == 7:
            res += "soixante-" + teens[u]
        elif t == 8:
            if u == 0:
                res += "quatre-vingts"
            else:
                res += "quatre-vingt-" + units[u]
        elif t == 9:
            res += "quatre-vingt-" + teens[u]
        else:
            if t > 0:
                res += tens[t]
                if u == 1:
                    res += " et "
                elif u > 0:
                    res += "-"
            res += units[u]
        
        return res.strip()

    if number == 0:
        return "zéro dinar"

    integer_part = int(number)
    decimal_part = int(round((number - integer_part) * 100))

    parts = []
    
    # Billions, Millions, Thousands, Units
    billions = integer_part // 1000000000
    millions = (integer_part % 1000000000) // 1000000
    thousands = (integer_part % 1000000) // 1000
    units_group = integer_part % 1000

    if billions > 0:
        parts.append(convert_group(billions) + (" milliard" if billions == 1 else " milliards"))
    if millions > 0:
        parts.append(convert_group(millions) + (" million" if millions == 1 else " millions"))
    if thousands > 0:
        if thousands == 1:
            parts.append("mille")
        else:
            parts.append(convert_group(thousands) + " mille")
    if units_group > 0:
        parts.append(convert_group(units_group))

    result = " ".join(parts).strip()
    result += " Dinars Algériens"

    if decimal_part > 0:
        result += " et " + convert_group(decimal_part) + " Centimes"

    return result.capitalize()
