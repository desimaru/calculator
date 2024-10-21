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
    while "" in array:
        array.remove("")
    return array


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


number = rcompile(r"^-?\d+\.?\d*?$")


def brackets(formula: list, bracket: str, result_type) -> list:
    """配列の括弧を探して計算する関数"""
    while bracket[0] in formula:
        left_bracket = index_of(formula, bracket[0])
        right_bracket = index_of(formula, bracket[1])
        if left_bracket != 0 and bool(number.match(str(formula[left_bracket - 1]))):
            in_bracket = calc(formula[left_bracket + 1 : right_bracket])
            del formula[left_bracket + 1 : right_bracket]
            formula[left_bracket] = in_bracket * result_type(
                formula.pop(left_bracket - 1)
            )
            formula.pop(left_bracket - 1)
        elif left_bracket != 0 and formula[left_bracket - 1] == "-":
            in_bracket = calc(formula[left_bracket + 1 : right_bracket])
            del formula[left_bracket + 1 : right_bracket]
            formula[left_bracket] = in_bracket * -1
            formula.pop(left_bracxket - 1)
        elif len(formula) - 1 != right_bracket and number.match(
            str(formula[right_bracket + 1])
        ):
            in_bracket = calc(formula[left_bracket + 1 : right_bracket])
            del formula[left_bracket + 1 : right_bracket]
            formula[left_bracket] = in_bracket * float(formula.pop(right_bracket + 1))
        else:
            formula[left_bracket] = calc(formula[left_bracket + 1 : right_bracket])
            del formula[left_bracket + 1 : right_bracket + 1]
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
    result_type = (
        int if all([not "." in i for i in formula]) and not "/" in formula else float
    )
    brackets(formula, "[]", result_type)
    brackets(formula, "{}", result_type)
    brackets(formula, "()", result_type)
    while "!" in formula:
        exclamation = formula.index("!")
        if not str(formula[exclamation - 1]).isdecimal():
            # 自然数ではない場合
            if int(formula[exclamation - 1]) < 0:
                # 負の数の場合
                formula[exclamation - 1] = (
                    f"-{factorial(abs(int(formula[exclamation-1])))}"
                )
                # 絶対値の階乗のマイナス
                formula.pop(exclamation)
        else:
            # 普通の階乗
            formula[exclamation - 1] = str(factorial(int(formula[exclamation - 1])))
            formula.pop(exclamation)
    while "^" in formula:
        hat = formula.index("^")
        formula[hat - 1] = str(
            result_type(formula[hat - 1]) ** result_type(formula.pop(hat + 1))
        )
        formula.pop(hat)
    while "*" in formula or "/" in formula or "%" in formula:
        asterisk = index_of(formula, "*")
        slash = index_of(formula, "/")
        percent = index_of(formula, "%")
        # 最初の演算子が/の時
        if slash != -1 and (
            (slash < asterisk or asterisk == -1) and (slash < percent or percent == -1)
        ):
            formula[slash - 1] = str(
                float(formula[slash - 1]) / float(formula.pop(slash + 1))
            )
            formula.pop(slash)
        elif asterisk != -1 and (asterisk < percent or percent == -1):
            formula[asterisk - 1] = str(
                result_type(formula[asterisk - 1])
                * result_type(formula.pop(asterisk + 1))
            )
            formula.pop(asterisk)
        elif percent != -1:
            formula[percent - 1] = str(
                result_type(formula[percent - 1])
                % result_type(formula.pop(percent + 1))
            )
            formula.pop(percent)
    while len(formula) > 1:
        formula[0] = str(result_type(formula[0]) + result_type(formula.pop(1)))
    return result_type(formula[0])


def calculator(str_formula: str) -> str:
    """渡された文字列を評価して返す関数

    Args:
        str_formula (str):評価したい文字列
    """
    if str_formula == "":
        return "0"
    # 文字列を数字と演算子で分ける
    if str(
        x := calc(
            del_empty(
                str_formula.replace("-", "+-")
                .replace("*", "+*+")
                .replace("/", "+/+")
                .replace("^", "+^+")
                .replace("!", "+!+")
                .replace("(", "+(+")
                .replace(")", "+)+")
                .replace("{", "+{+")
                .replace("}", "+}+")
                .replace("[", "+[+")
                .split("+")
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
