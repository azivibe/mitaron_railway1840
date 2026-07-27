#import "style.typ": *
#let show-solutions = false
#let maybe-solution(title, body) = if show-solutions { solution(title, body) } else { none }
#let maybe-key(body) = if show-solutions { key(body) } else { none }
#let maybe-caution(body) = if show-solutions { caution(body) } else { none }
#include "content.typ"
