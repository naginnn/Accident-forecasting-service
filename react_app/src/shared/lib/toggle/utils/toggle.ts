export const toggle = <T>(curr: T, name1: T, name2: T) => {
    return curr === name1 ? name2 : name1;
}
