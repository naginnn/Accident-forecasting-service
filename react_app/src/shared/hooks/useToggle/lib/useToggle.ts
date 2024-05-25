import {useState, useCallback} from 'react';

export const useToggle = (initValue: boolean = false) => {
    const [value, setValue] = useState<boolean>(initValue);

    const on = useCallback(() => {
        setValue(true)
    }, [])

    const off = useCallback(() => {
        setValue(false)
    }, [])

    const toggle = useCallback(() => {
        setValue(prev => !prev)
    }, [setValue])

    return ({on, off, toggle, value});
}
