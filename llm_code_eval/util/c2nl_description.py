NA_PROMPT = """\
Descriptions
Scores: 1-5 (from bad to good)

The human evaluation criterions are shown as follows:

Naturalness: measuring documentation with the features of natural languages: evaluate the grammaticality and fluency of generated documentation, ignoring contents

Special Symbols:
1. STR_: means a string (for example: System.out.println("Hello Word") --> System.out.println(STR_))
2. NUM_: means a number (for example: for(int i=0;i<10;i++) --> for(int i=NUM_; i<NUM_;i++))
3. BOOL_: means a boolean value (for example: if(True) -->if(BOOL_))
"""

EX_PROMPT = """\
Descriptions
Scores: 1-5 (from bad to good)

The human evaluation criterions are shown as follows:

Expressiveness: measuring documentation with the features of natural languages: evaluate the documentation's readability and understandability in the respect of their way of description, ignoring contents

Special Symbols:
1. STR_: means a string (for example: System.out.println("Hello Word") --> System.out.println(STR_))
2. NUM_: means a number (for example: for(int i=0;i<10;i++) --> for(int i=NUM_; i<NUM_;i++))
3. BOOL_: means a boolean value (for example: if(True) -->if(BOOL_))
"""

CA_PROMPT = """\
Descriptions
Scores: 1-5 (from bad to good)

The human evaluation criterions are shown as follows:

Content Adequacy: evaluating the generated documentation on contents: measure the amount of contents carried over from the input to the NL documentation, ignoring fluency in language.

Special Symbols:
1. STR_: means a string (for example: System.out.println("Hello Word") --> System.out.println(STR_))
2. NUM_: means a number (for example: for(int i=0;i<10;i++) --> for(int i=NUM_; i<NUM_;i++))
3. BOOL_: means a boolean value (for example: if(True) -->if(BOOL_))
"""

CON_PROMPT = """\
Descriptions
Scores: 1-5 (from bad to good)

The human evaluation criterions are shown as follows:

Conciseness: evaluating the generated documentation on contents: measure to what extent the documentation contains the unnecessary information.

Special Symbols:
1. STR_: means a string (for example: System.out.println("Hello Word") --> System.out.println(STR_))
2. NUM_: means a number (for example: for(int i=0;i<10;i++) --> for(int i=NUM_; i<NUM_;i++))
3. BOOL_: means a boolean value (for example: if(True) -->if(BOOL_))
"""

USE_PROMPT = """\
Descriptions
Scores: 1-5 (from bad to good)

The human evaluation criterions are shown as follows:

Usefulness: measure to what extent the generated documentation is useful for developers to understand code. 

Special Symbols:
1. STR_: means a string (for example: System.out.println("Hello Word") --> System.out.println(STR_))
2. NUM_: means a number (for example: for(int i=0;i<10;i++) --> for(int i=NUM_; i<NUM_;i++))
3. BOOL_: means a boolean value (for example: if(True) -->if(BOOL_))
"""

CU_PROMPT = """\
Descriptions
Scores: 1-5 (from bad to good)

The human evaluation criterions are shown as follows:

Code understandability: evaluate to what degree does the generated documentation help developers understand the programs.

Special Symbols:
1. STR_: means a string (for example: System.out.println("Hello Word") --> System.out.println(STR_))
2. NUM_: means a number (for example: for(int i=0;i<10;i++) --> for(int i=NUM_; i<NUM_;i++))
3. BOOL_: means a boolean value (for example: if(True) -->if(BOOL_))
"""

NEC_PROMPT = """\
Descriptions
Scores: 1-5 (from bad to good)

The human evaluation criterions are shown as follows:

Usefulness: measure to what extent the generated documentation are necessary.

Special Symbols:
1. STR_: means a string (for example: System.out.println("Hello Word") --> System.out.println(STR_))
2. NUM_: means a number (for example: for(int i=0;i<10;i++) --> for(int i=NUM_; i<NUM_;i++))
3. BOOL_: means a boolean value (for example: if(True) -->if(BOOL_))
"""


PROMPTS = {
    "naturalness": NA_PROMPT,
    "expressiveness": EX_PROMPT,
    "content_adequacy": CA_PROMPT,
    "conciseness": CON_PROMPT,
    "usefulness": USE_PROMPT,
    "code_understandability": CU_PROMPT,
    "necessity": NEC_PROMPT,
}