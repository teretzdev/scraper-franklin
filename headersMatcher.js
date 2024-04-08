const patterns = {
    fullNamePattern: /([A-Z]+, [A-Z ]+)/,
    addressPattern: /(\d+ [A-Z\s]+),\s*([A-Z\s]+),\s*(MO)\s*(\d+)/,
    arrestStatusPattern: /(ARRESTED ON\s+WARRANT|HOLD FOR USMS|24 HOUR HOLD)/,
    chargePattern: /([A-Z\s]+)\n(\d{2}[A-Z]{2}-CR\d{5})/g,
};

module.exports = patterns;
