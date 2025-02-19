#!/usr/bin/env python3
from math import factorial
from re import compile as rcompile


def del_empty(array: list) -> list:
    """配列の空要素を消す関数

    Args:
        lis (list[Any]): 空要素を消したい配列

    Returns:
        list[Any]: 空要素が消えた配列
    """
    return [i for i in array if i != ""]


def index_of(array: list, element) -> int:
    """要素の位置を返す関数

    任意の要素が配列に含まれていない場合に-1を返す関数

    Args:
        array (list):探したい配列
        element (any):探したい要素
    Returns:
        int: 要素の位置 無い場合は-1を返す
    """
    if element in array:
        return array.index(element)
    return -1


number_bracket = rcompile(r"(\d+)(\(|\{|\[)")
parse = rcompile(r"(\*|/|%|\^|!|\(|\)|\{|\}|\[|\])")


def brackets(formula: list, bracket: str) -> list:
    """配列の括弧を探して計算する関数"""
    while bracket[0] in formula:
        left_bracket = index_of(formula, bracket[0])
        right_bracket = index_of(formula, bracket[1])
        formula[left_bracket] = calc(formula[left_bracket + 1: right_bracket])
        del formula[left_bracket + 1: right_bracket + 1]
    return formula


def calc(formula: list) -> float:
    """引数に渡された式を評価する関数

    Args:
        formula (list):式
    Retuns:
        float:計算結果
    Note:
        優先順位:
            1:[]
            2:{}
            3:()
            4:!
            5:^
            6:*、/、%
            7:+、-
    """
    # formulaに小数点とスラッシュが含まれていない場合は計算結果を整数にする
    result_type = int if (
        all("." not in str(i) for i in formula) and "/" not in formula
    ) else float
    brackets(formula, "[]")
    brackets(formula, "{}")
    brackets(formula, "()")
    while "!" in formula:
        exclamation = formula.index("!")
        if not str(formula[exclamation - 1]).isdecimal():
            # 自然数ではない場合
            if int(formula[exclamation - 1]) < 0:
                # 負の数の場合
                formula[exclamation - 1] = (
                    -factorial(abs(int(formula[exclamation-1])))
                )
                # 絶対値の階乗のマイナス
                formula.pop(exclamation)
        else:
            # 普通の階乗
            formula[exclamation - 1] = str(
                factorial(int(formula[exclamation - 1]))
            )
            formula.pop(exclamation)
    while "^" in formula:
        hat = formula.index("^")
        formula[hat - 1] = result_type(formula[hat - 1]) ** result_type(
            formula.pop(hat + 1)
        )
        formula.pop(hat)
    while "*" in formula or "/" in formula or "%" in formula:
        asterisk = index_of(formula, "*")
        slash = index_of(formula, "/")
        percent = index_of(formula, "%")
        # 最初の演算子が/の時
        if slash != -1 and ((slash < asterisk or asterisk == -1) and (
            slash < percent or percent == -1
        )
        ):
            formula[slash - 1] = str(
                float(formula[slash - 1]) / float(formula.pop(slash + 1))
            )
            formula.pop(slash)
        elif asterisk != -1 and (asterisk < percent or percent == -1):
            formula[asterisk - 1] = result_type(formula[asterisk - 1]) * (
                result_type(formula.pop(asterisk + 1))
            )
            formula.pop(asterisk)
        elif percent != -1:
            formula[percent - 1] = result_type(formula[percent - 1]) % (
                result_type(formula.pop(percent + 1))
            )
            formula.pop(percent)
    return result_type(sum(result_type(i) for i in formula))


def calculator(str_formula: str) -> str:
    """渡された文字列を評価して返す関数

    Args:
        str_formula (str):評価したい文字列
    """
    if str_formula == "":
        return "0"
    # 文字列を数字と演算子で分ける
    if "(" in str_formula or "{" in str_formula or "[" in str_formula:
        str_formula = number_bracket.sub(r"\1*\2", str_formula)
    if str(
        x := calc(
            del_empty(
                parse.sub(
                    r"+\1+",
                    str_formula.replace(" ", "").replace("-", "+-")
                ).split("+")
            )
        )
    ).endswith(".0"):
        return str(int(x))
    return str(x)


print("数式を打ってください。(quitで終了)")
while (a := input(">")) != "quit":
    try:
        print(calculator(a))
    except (ValueError, IndexError):
        print("無効な値です")
    except OverflowError:
        print("オーバーフロー")
    except ZeroDivisionError:
        print("ゼロ除算が発生しました")
