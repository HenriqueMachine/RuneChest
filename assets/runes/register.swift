// Registers a font file with CoreText for the user (a copy to ~/Library/Fonts is not always picked up).
// Run: swift assets/runes/register.swift ~/Library/Fonts/RuneChestRunes.ttf
import CoreText
import Foundation
let url = URL(fileURLWithPath: CommandLine.arguments[1]) as CFURL
var err: Unmanaged<CFError>?
let ok = CTFontManagerRegisterFontsForURL(url, .user, &err)
print("register:", ok, err.map { CFErrorCopyDescription($0.takeRetainedValue()) as String } ?? "")
let all = CTFontManagerCopyAvailableFontFamilyNames() as! [String]
print("registered now:", all.contains("RuneChest Runes"))
