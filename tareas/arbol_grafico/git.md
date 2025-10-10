<!--
archivo     : git.md
fecha       : 22.09.2025
autor       : Lorgio Añez J.
contenido   : Comandos utiles de git
-->

#### Comandos utiles de git

- Ver el estado de la rama actual

`git status`

- Adicionar los cambios de la rama actual al `stage`

`git add .`

- Crear un commit para actualizar la rama con los cambios del `stage`

`git commit -m "1er commit arbol_grafico"`

- Crear un rama

`git brach arbol_grafico`

- Cambiarse a una rama

`git checkout arbol_grafico`

- Actualizar el repositorio actual al remoto en github

`git add .`
`git commit -m "Actualizado repositorio remoto"`
`git push origin arbol_grafico`
`

#### Eliminar archivos de todas las ramas del github (revisar procedimiento)

- Si el archivo existe en varias ramas, puedes hacer lo siguiente:
  - Eliminar un archivo de una rama (branch1, branch2, branch3) en github
  - Opcionalmente se puede eliminar localmente, y actualizar en el remoto

`git checkout nombre-de-la-rama`
`git rm --cached nombre-del-archivo.ext`
`git commit -m "Eliminando nombre-del-archivo.ext de la rama nombre-de-la-rama"`
`git push origin nombre-de-la-rama`
