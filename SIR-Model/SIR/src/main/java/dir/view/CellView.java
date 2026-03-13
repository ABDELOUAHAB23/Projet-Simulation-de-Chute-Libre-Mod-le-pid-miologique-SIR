package dir.view;

import dir.model.State;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

/**
 * The CellView class represents a visual cell in the SIR model simulation.
 * It extends the Rectangle class and provides functionality to update its color
 * based on the state of the cell (SUSCEPTIBLE, INFECTIOUS, or RECOVERED).
 */
public class CellView extends Rectangle {

    // 👇 Ajout des constantes de couleurs manquantes
    private static final Color SUSCEPTIBLE_COLOR = Color.LIGHTBLUE;
    private static final Color INFECTIOUS_COLOR = Color.CRIMSON;
    private static final Color RECOVERED_COLOR = Color.LIGHTGREEN;

    public CellView(double width, double height, State state) {
        super(width, height);
        updateColor(state);
    }

    public final void updateColor(State state) {
        switch (state) {
            case SUSCEPTIBLE -> setFill(SUSCEPTIBLE_COLOR);
            case INFECTIOUS -> setFill(INFECTIOUS_COLOR);
            case RECOVERED -> setFill(RECOVERED_COLOR);
        }
    }
}
