module.exports = {
    root: true,
    env: {
        node: true,
    },
    extends: [
        "plugin:vue/essential",
        "eslint:recommended",
        "@vue/typescript/recommended",
        "@vue/prettier",
        "@vue/prettier/@typescript-eslint",
    ],
    parserOptions: {
        ecmaVersion: 2020,
    },
    rules: {
        "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
        "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
        "indent": [true, "spaces", 2],
        "quotemark": [true, "single"],
        "no-trailing-whitespace": [true, "always"],
        "prefer-const": [true, { "destructuring": "any" }],
        "semicolon": [true, "always"],
        "space-before-function-paren": [true, "never"],
        "trailing-comma": [false],
        "comma-dangle": ["error", "only-multiline"],
        "typedef": [true, "call-signature", "property-declaration"],
        "@typescript-eslint/no-explicit-any": 0,
    }
}