import enum

def IsSpecial(value):
    if value == "(" or value == ")" or value == "[" or value == "]" or value == "{" or value == "}" or value == "." or value == "," or value == ":" or value == ";" or value == "=" or value == "+" or value == "-" or value == "*" or value == "/" or value == "!" or value == "?" or value == "@" or value == "#" or value == "$" or value == "%" or value == "&":
        return True
    else:
        return False

def IsNumber(value):
    if value == "0" or value == "1" or value == "2" or value == "3" or value == "4" or value == "5" or value == "6" or value == "7" or value == "8" or value == "9" or value == "0" or value == ".":
        return True
    else:
        return False

class TokenType(enum.Enum):
    NULL = 0
    EOF = 1

    IDENTIFIER = 2

    LITERAL_STRING = 3
    LITERAL_NUMBER = 4
    LITERAL_BOOL = 5

    LPAREN = 6
    RPAREN = 7
    LBRACKET = 8
    RBRACKET = 9
    LBRACE = 10
    RBRACE = 11

    PERIOD = 12
    COMMA = 13
    COLON = 14
    SEMICOLON = 15
    EQUALS = 16
    PLUS = 17
    MINUS = 18
    ASTERISK = 19
    SLASH = 20
    EXCLAMATION = 21
    QUESTION = 22
    AT = 23
    HASH = 24
    DOLLAR = 25
    PERCENT = 26
    AMPERSAND = 27

    # keyword tokens
    KW_VAR_DEF = 39
    KW_IF = 30
    KW_ELSE = 31
    KW_ELSEIF = 32

class Token:
    def __init__(self, value, type = None):
        self.value = value
        self.type = type

    def ConvertSpecial(self):
        if self.value == "(":
            self.type = TokenType.LPAREN
        elif self.value == ")":
            self.type = TokenType.RPAREN
        elif self.value == "[":
            self.type = TokenType.LBRACKET
        elif self.value == "]":
            self.type = TokenType.RBRACKET
        elif self.value == "{":
            self.type = TokenType.LBRACE
        elif self.value == "}":
            self.type = TokenType.RBRACE
        elif self.value == ".":
            self.type = TokenType.PERIOD
        elif self.value == ",":
            self.type = TokenType.COMMA
        elif self.value == ":":
            self.type = TokenType.COLON
        elif self.value == ";":
            self.type = TokenType.SEMICOLON
        elif self.value == "=":
            self.type = TokenType.EQUALS
        elif self.value == "+":
            self.type = TokenType.PLUS
        elif self.value == "-":
            self.type = TokenType.MINUS
        elif self.value == "*":
            self.type = TokenType.ASTERISK
        elif self.value == "/":
            self.type = TokenType.SLASH
        elif self.value == "!":
            self.type = TokenType.EXCLAMATION
        elif self.value == "?":
            self.type = TokenType.QUESTION
        elif self.value == "@":
            self.type = TokenType.AT
        elif self.value == "#":
            self.type = TokenType.HASH
        elif self.value == "%":
            self.type = TokenType.PERCENT
        elif self.value == "&":
            self.type = TokenType.AMPERSAND

    def ConvertToken(self):
        if self.value == TokenType.LPAREN:
            self.type = "("
        elif self.value == TokenType.RPAREN:
            self.type = ")"
        elif self.value == TokenType.LBRACKET:
            self.type = "["
        elif self.value == TokenType.RBRACKET:
            self.type = "]"
        elif self.value == TokenType.LBRACE:
            self.type = "{"
        elif self.value == TokenType.RBRACE:
            self.type = "}"
        elif self.value == TokenType.PERIOD:
            self.type = "."
        elif self.value == TokenType.COMMA:
            self.type = ","
        elif self.value == TokenType.COLON:
            self.type = ":"
        elif self.value == TokenType.SEMICOLON:
            self.type = ";"
        elif self.value == TokenType.EQUALS:
            self.type = "="
        elif self.value == TokenType.PLUS:
            self.type = "+"
        elif self.value == TokenType.MINUS:
            self.type = "-"
        elif self.value == TokenType.ASTERISK:
            self.type = "*"
        elif self.value == TokenType.SLASH:
            self.type = "/"
        elif self.value == TokenType.EXCLAMATION:
            self.type = "!"
        elif self.value == TokenType.QUESTION:
            self.type = "?"
        elif self.value == TokenType.AT:
            self.type = "@"
        elif self.value == TokenType.HASH:
            self.type = "#"
        elif self.value == TokenType.PERCENT:
            self.type = "%"
        elif self.value == TokenType.AMPERSAND:
            self.type = "&"

class Tokenizer:
    def tokenize(self, file):
        file = open(file, "r", -1, "utf-8")
        curText = ""
        tokens = []

        for line in file.readlines():
            for char in line:
                curText = curText.strip("\n")

                # space
                if char == " ":
                    continue

                # special character
                if IsSpecial(char):
                    
                    if curText != "":
                        curToken = Token(curText)

                        # ======== multiple character integers ========
                        if IsNumber(curToken.value[0]):
                            num = ""

                            for char2 in curToken.value:
                                if (not IsNumber(char2))
                                    break
                                
                                num += char2
                            
                            t = Token(int(num), TokenType.LITERAL_NUMBER)
                            tokens.append(t)

                            # this next part seemed to fix an issue with
                            # special characters after a number not being
                            # tokenized so i'll keep it here
                            curText = ""
                            curText += char

                            curToken = Token(curText)
                            curToken.ConvertSpecial()
                            tokens.append(curToken)

                            curText = ""
                            continue


                        # ======== keywords ========
                        if curToken.value == "if":
                            curToken.type = TokenType.KW_IF
                        elif curToken.value == "else":
                            curToken.type = TokenType.KW_ELSE
                        elif curToken.value == "elseif":
                            curToken.type = TokenType.KW_ELSEIF
                        elif curToken.value[0] == "\"":
                            curToken.type = TokenType.LITERAL_STRING
                        elif curToken.value == "newv":
                            curToken.type = TokenType.KW_VAR_DEF
                        elif curToken.value == "null":
                            curToken.type = TokenType.NULL
                        elif curToken.value == "true" or curToken.value == "false":
                            curToken.type = TokenType.LITERAL_BOOL
                        else:
                            curToken.type = TokenType.IDENTIFIER

                        tokens.append(curToken)


                    # ======== special characters ========
                    curText = ""
                    curText += char

                    curToken = Token(curText)
                    curToken.ConvertSpecial()
                    tokens.append(curToken)

                    curText = ""
                    continue

                curText += char

        file.close()
        return tokens


def runCode(file):
    t = Tokenizer()
    tokenCount = 0
    tokens = t.tokenize(file)

    # the code execution will start here
    for i in range(len(tokens)):
        curToken = tokens[i] 

        tokenCount += 1
        
    # debug
    for token in tokens:
        print(f"[{token.value}]", end = "")
        
    print("\n")
    
