library(tidyverse)

mesh <- read_csv("mesh.csv") |>
	head(30)
	#filter( count >= 10 )
keys <- read_csv("keywords.csv") |>
	head(30)
	#filter( count >= 4 )

mesh <- mesh |>
	mutate(
	       key = factor( key, levels = rev(mesh$key) )
        )
keys <- keys |>
	mutate(
	       key = factor( key, levels = rev(keys$key) )
        )

g1 <- mesh |> ggplot( aes( y = key, x = count ) ) +
	       geom_col() +
	       geom_text( aes( label = count ), hjust = -1 ) +
	       ggtitle("MESH kategorie hodnocených článků 2022–2023") +
	       xlab("počet") +
	       ylab("kategorie") +
	       theme( text = element_text(size = 30) )
g2 <- keys |> ggplot( aes( y = key, x = count ) ) +
	       geom_col() +
	       geom_text( aes( label = count ), hjust = -1 ) +
	       ggtitle("Klíčová slova hodnocených článků 2022–2023") +
	       xlab("počet") +
	       ylab("klíčová slova") +
	       theme( text = element_text(size = 30) )
