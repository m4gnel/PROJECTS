package com.agrisage.app.ui.screens

import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Agriculture
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Grass
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Pets
import androidx.compose.material.icons.filled.ShoppingBasket
import androidx.compose.material.icons.filled.WaterDrop
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.agrisage.app.ui.components.AgriBottomNav
import com.agrisage.app.ui.components.tactilePress
import com.agrisage.app.ui.theme.WireAlert
import com.agrisage.app.ui.theme.WireAlertPale
import com.agrisage.app.ui.theme.WireBorder
import com.agrisage.app.ui.theme.WireGold
import com.agrisage.app.ui.theme.WireGoldPale
import com.agrisage.app.ui.theme.WireLeaf
import com.agrisage.app.ui.theme.WireLeafPale
import com.agrisage.app.ui.theme.WireSage
import com.agrisage.app.ui.theme.WireSageDeep
import com.agrisage.app.ui.theme.WireSky
import com.agrisage.app.ui.theme.WireSkyPale
import com.agrisage.app.ui.theme.WireSoil
import com.agrisage.app.ui.theme.WireSoilPale
import com.agrisage.app.ui.theme.WireSurface
import com.agrisage.app.ui.theme.WireSurface2
import com.agrisage.app.ui.theme.WireTextPrimary
import com.agrisage.app.ui.theme.WireTextSecondary
import com.agrisage.app.ui.theme.WireWhite

private enum class FarmSection(val label: String) {
    OVERVIEW("Overview"),
    CROPS("Crops"),
    LIVESTOCK("Livestock"),
    WATER("Water"),
    STORAGE("Storage")
}

private data class FarmArea(
    val id: String,
    val name: String,
    val detail: String,
    val icon: ImageVector,
    val surfaceColor: Color,
    val iconTint: Color,
    val xFraction: Float,
    val yFraction: Float
)

private val farmAreas = listOf(
    FarmArea(
        id = "house",
        name = "House",
        detail = "Home base",
        icon = Icons.Default.Home,
        surfaceColor = WireGoldPale,
        iconTint = WireSoil,
        xFraction = 0.05f,
        yFraction = 0.05f
    ),
    FarmArea(
        id = "storage",
        name = "Storage",
        detail = "Tools & harvest",
        icon = Icons.Default.ShoppingBasket,
        surfaceColor = WireSurface,
        iconTint = WireSageDeep,
        xFraction = 0.67f,
        yFraction = 0.05f
    ),
    FarmArea(
        id = "tomatoes",
        name = "Tomatoes",
        detail = "2 beds",
        icon = Icons.Default.Agriculture,
        surfaceColor = WireAlertPale,
        iconTint = WireAlert,
        xFraction = 0.03f,
        yFraction = 0.36f
    ),
    FarmArea(
        id = "vegetables",
        name = "Vegetables",
        detail = "Kitchen garden",
        icon = Icons.Default.Grass,
        surfaceColor = WireLeafPale,
        iconTint = WireSage,
        xFraction = 0.33f,
        yFraction = 0.37f
    ),
    FarmArea(
        id = "corn",
        name = "Corn",
        detail = "East plot",
        icon = Icons.Default.Eco,
        surfaceColor = WireGoldPale,
        iconTint = WireGold,
        xFraction = 0.67f,
        yFraction = 0.36f
    ),
    FarmArea(
        id = "water",
        name = "Water",
        detail = "Pond & pump",
        icon = Icons.Default.WaterDrop,
        surfaceColor = WireSkyPale,
        iconTint = WireSky,
        xFraction = 0.05f,
        yFraction = 0.70f
    ),
    FarmArea(
        id = "animals",
        name = "Animals",
        detail = "Barn & pasture",
        icon = Icons.Default.Pets,
        surfaceColor = WireSoilPale,
        iconTint = WireSoil,
        xFraction = 0.66f,
        yFraction = 0.70f
    )
)

/**
 * Farm overview with a warm, map-led layout inspired by the supplied reference videos.
 * The map areas are real touch targets: selecting one updates the helper card and chip context.
 */
@Composable
fun FieldsScreen(navController: NavController) {
    var selectedSection by remember { mutableStateOf(FarmSection.OVERVIEW) }
    var selectedAreaId by remember { mutableStateOf<String?>(null) }

    val selectedArea = farmAreas.firstOrNull { it.id == selectedAreaId }

    Scaffold(
        containerColor = WireWhite,
        topBar = {
            FarmOverviewTopBar(
                onNavigateBack = { navController.popBackStack() }
            )
        },
        bottomBar = {
            AgriBottomNav(
                currentRoute = "fields",
                onNavigate = { route ->
                    when (route) {
                        "home" -> navController.navigate(com.agrisage.app.navigation.Home) {
                            popUpTo(com.agrisage.app.navigation.Home) { inclusive = true }
                        }
                        "advisor" -> navController.navigate(com.agrisage.app.navigation.Advisor)
                        "weather" -> navController.navigate(com.agrisage.app.navigation.Weather)
                        "profile" -> navController.navigate(com.agrisage.app.navigation.Profile)
                    }
                }
            )
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(WireWhite),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 18.dp, bottom = 28.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                FarmSectionChips(
                    selectedSection = selectedSection,
                    onSectionSelected = { section ->
                        selectedSection = section
                        selectedAreaId = when (section) {
                            FarmSection.OVERVIEW -> null
                            FarmSection.CROPS -> "tomatoes"
                            FarmSection.LIVESTOCK -> "animals"
                            FarmSection.WATER -> "water"
                            FarmSection.STORAGE -> "storage"
                        }
                    }
                )
            }

            item {
                Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(
                        text = "Your farm plan",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = WireTextPrimary
                    )
                    Text(
                        text = selectedArea?.let { "${it.name} selected · tap another area to explore" }
                            ?: "A simple view of every area on your farm",
                        fontSize = 13.sp,
                        color = WireTextSecondary
                    )
                }
            }

            item {
                FarmPlanMap(
                    selectedAreaId = selectedAreaId,
                    onAreaSelected = { area ->
                        selectedAreaId = area.id
                        selectedSection = when (area.id) {
                            "tomatoes", "vegetables", "corn" -> FarmSection.CROPS
                            "animals" -> FarmSection.LIVESTOCK
                            "water" -> FarmSection.WATER
                            "storage" -> FarmSection.STORAGE
                            else -> FarmSection.OVERVIEW
                        }
                    }
                )
            }

            item {
                FarmHelperCard(selectedArea = selectedArea)
            }
        }
    }
}

@Composable
private fun FarmOverviewTopBar(onNavigateBack: () -> Unit) {
    Surface(
        color = WireWhite,
        shadowElevation = 0.5.dp,
        modifier = Modifier
            .fillMaxWidth()
            .statusBarsPadding()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Surface(
                modifier = Modifier
                    .size(48.dp)
                    .semantics {
                        contentDescription = "Go back"
                        role = Role.Button
                    }
                    .tactilePress(
                        scaleDown = 0.94f,
                        onClickLabel = "Go back",
                        onClick = onNavigateBack
                    ),
                shape = CircleShape,
                color = WireSurface,
                border = BorderStroke(1.dp, WireBorder)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = null,
                        tint = WireTextPrimary,
                        modifier = Modifier.size(21.dp)
                    )
                }
            }

            Spacer(Modifier.width(12.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Green Valley Farm",
                    fontSize = 22.sp,
                    lineHeight = 26.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = WireTextPrimary
                )
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(top = 3.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.LocationOn,
                        contentDescription = null,
                        tint = WireSage,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(Modifier.width(4.dp))
                    Text(
                        text = "Nashik, Maharashtra",
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Medium,
                        color = WireTextSecondary
                    )
                }
            }

            Surface(
                shape = CircleShape,
                color = WireLeafPale,
                modifier = Modifier.size(42.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Default.Eco,
                        contentDescription = "Farm overview",
                        tint = WireSageDeep,
                        modifier = Modifier.size(21.dp)
                    )
                }
            }
        }
    }
}

@Composable
private fun FarmSectionChips(
    selectedSection: FarmSection,
    onSectionSelected: (FarmSection) -> Unit
) {
    LazyRow(
        modifier = Modifier
            .fillMaxWidth()
            .semantics { contentDescription = "Farm sections" },
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        contentPadding = PaddingValues(end = 8.dp)
    ) {
        items(FarmSection.values().size) { index ->
            val section = FarmSection.values()[index]
            FarmSectionChip(
                label = section.label,
                selected = selectedSection == section,
                onClick = { onSectionSelected(section) }
            )
        }
    }
}

@Composable
private fun FarmSectionChip(
    label: String,
    selected: Boolean,
    onClick: () -> Unit
) {
    val backgroundColor by animateColorAsState(
        targetValue = if (selected) WireSageDeep else WireWhite,
        label = "farm_section_background"
    )
    val textColor by animateColorAsState(
        targetValue = if (selected) WireWhite else WireTextSecondary,
        label = "farm_section_text"
    )

    Surface(
        color = backgroundColor,
        shape = RoundedCornerShape(15.dp),
        border = if (selected) null else BorderStroke(1.dp, WireBorder),
        shadowElevation = if (selected) 2.dp else 0.dp,
        modifier = Modifier
            .heightIn(min = 48.dp)
            .semantics {
                contentDescription = "$label section"
                role = Role.Button
                stateDescription = if (selected) "Selected" else "Not selected"
            }
            .tactilePress(
                scaleDown = 0.95f,
                onClickLabel = "Open $label section",
                onClick = onClick
            )
    ) {
        Box(
            modifier = Modifier.padding(horizontal = 17.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = label,
                fontSize = 13.sp,
                fontWeight = if (selected) FontWeight.Bold else FontWeight.SemiBold,
                color = textColor
            )
        }
    }
}

@Composable
private fun FarmPlanMap(
    selectedAreaId: String?,
    onAreaSelected: (FarmArea) -> Unit
) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(360.dp)
            .clip(RoundedCornerShape(28.dp))
            .background(WireSurface2)
            .semantics {
                contentDescription = "Interactive farm plan with seven labeled areas"
            }
    ) {
        Canvas(modifier = Modifier.matchParentSize()) {
            drawFarmPlan()
        }

        Surface(
            color = WireWhite.copy(alpha = 0.9f),
            shape = RoundedCornerShape(12.dp),
            shadowElevation = 1.dp,
            modifier = Modifier
                .align(Alignment.TopCenter)
                .padding(top = 14.dp)
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 10.dp, vertical = 7.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "N",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = WireSageDeep
                )
                Spacer(Modifier.width(5.dp))
                Text(
                    text = "Farm plan",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.SemiBold,
                    color = WireTextSecondary
                )
            }
        }

        BoxWithConstraints(modifier = Modifier.matchParentSize()) {
            farmAreas.forEach { area ->
                FarmAreaButton(
                    area = area,
                    selected = selectedAreaId == area.id,
                    onClick = { onAreaSelected(area) },
                    modifier = Modifier
                        .align(Alignment.TopStart)
                        .offset(
                            x = maxWidth * area.xFraction,
                            y = maxHeight * area.yFraction
                        )
                )
            }
        }
    }
}

@Composable
private fun FarmAreaButton(
    area: FarmArea,
    selected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val containerColor = if (selected) WireWhite else area.surfaceColor.copy(alpha = 0.96f)
    val borderColor = if (selected) WireSageDeep else WireWhite.copy(alpha = 0.8f)

    Surface(
        color = containerColor,
        shape = RoundedCornerShape(17.dp),
        border = BorderStroke(if (selected) 2.dp else 1.dp, borderColor),
        shadowElevation = if (selected) 5.dp else 2.dp,
        modifier = modifier
            .width(92.dp)
            .heightIn(min = 56.dp)
            .semantics {
                contentDescription = "${area.name} area. ${area.detail}"
                role = Role.Button
                stateDescription = if (selected) "Selected" else "Tap to explore"
            }
            .tactilePress(
                scaleDown = 0.94f,
                onClickLabel = "Explore ${area.name}",
                onClick = onClick
            )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(30.dp)
                    .clip(CircleShape)
                    .background(area.surfaceColor),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = area.icon,
                    contentDescription = null,
                    tint = area.iconTint,
                    modifier = Modifier.size(17.dp)
                )
            }
            Spacer(Modifier.width(6.dp))
            Text(
                text = area.name,
                fontSize = 12.sp,
                lineHeight = 14.sp,
                fontWeight = FontWeight.Bold,
                color = WireTextPrimary,
                maxLines = 1
            )
        }
    }
}

@Composable
private fun FarmHelperCard(selectedArea: FarmArea?) {
    val message = selectedArea?.let {
        "${it.name} is selected. Tap another area to keep exploring."
    } ?: "Tap an area on the map to explore your farm."

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .semantics { contentDescription = "Farm map helper. $message" },
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = WireSageDeep),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 15.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Surface(
                color = WireLeafPale,
                shape = CircleShape,
                modifier = Modifier.size(44.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Default.LocationOn,
                        contentDescription = null,
                        tint = WireSageDeep,
                        modifier = Modifier.size(21.dp)
                    )
                }
            }
            Spacer(Modifier.width(12.dp))
            Column(verticalArrangement = Arrangement.spacedBy(3.dp)) {
                Text(
                    text = "Explore your farm",
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = WireWhite
                )
                Text(
                    text = message,
                    fontSize = 13.sp,
                    lineHeight = 18.sp,
                    color = WireWhite.copy(alpha = 0.84f)
                )
            }
        }
    }
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawFarmPlan() {
    val w = size.width
    val h = size.height

    drawRect(
        brush = Brush.linearGradient(
            colors = listOf(WireSurface2, WireWhite),
            start = Offset(0f, 0f),
            end = Offset(w, h)
        )
    )

    val upperMeadow = Path().apply {
        moveTo(0f, h * 0.04f)
        cubicTo(w * 0.25f, h * 0.16f, w * 0.44f, h * 0.02f, w * 0.72f, h * 0.12f)
        cubicTo(w * 0.86f, h * 0.16f, w * 0.96f, h * 0.10f, w, h * 0.18f)
        lineTo(w, h * 0.42f)
        cubicTo(w * 0.75f, h * 0.36f, w * 0.48f, h * 0.49f, 0f, h * 0.39f)
        close()
    }
    drawPath(upperMeadow, color = WireLeafPale.copy(alpha = 0.56f))

    val lowerMeadow = Path().apply {
        moveTo(0f, h * 0.62f)
        cubicTo(w * 0.25f, h * 0.54f, w * 0.48f, h * 0.67f, w * 0.73f, h * 0.58f)
        cubicTo(w * 0.86f, h * 0.54f, w * 0.95f, h * 0.62f, w, h * 0.58f)
        lineTo(w, h)
        lineTo(0f, h)
        close()
    }
    drawPath(lowerMeadow, color = WireLeafPale.copy(alpha = 0.38f))

    val mainPath = Path().apply {
        moveTo(w * 0.48f, 0f)
        cubicTo(w * 0.45f, h * 0.20f, w * 0.56f, h * 0.28f, w * 0.48f, h * 0.46f)
        cubicTo(w * 0.41f, h * 0.64f, w * 0.48f, h * 0.77f, w * 0.53f, h)
    }
    drawPath(
        path = mainPath,
        color = WireSoilPale.copy(alpha = 0.94f),
        style = androidx.compose.ui.graphics.drawscope.Stroke(
            width = 18.dp.toPx(),
            cap = StrokeCap.Round,
            join = StrokeJoin.Round
        )
    )
    drawPath(
        path = mainPath,
        color = WireSoil.copy(alpha = 0.17f),
        style = androidx.compose.ui.graphics.drawscope.Stroke(
            width = 2.dp.toPx(),
            cap = StrokeCap.Round,
            join = StrokeJoin.Round
        )
    )

    val crossPath = Path().apply {
        moveTo(0f, h * 0.53f)
        cubicTo(w * 0.27f, h * 0.48f, w * 0.51f, h * 0.52f, w, h * 0.46f)
    }
    drawPath(
        path = crossPath,
        color = WireSoilPale.copy(alpha = 0.85f),
        style = androidx.compose.ui.graphics.drawscope.Stroke(
            width = 14.dp.toPx(),
            cap = StrokeCap.Round,
            join = StrokeJoin.Round
        )
    )

    val cropLineColor = WireSage.copy(alpha = 0.28f)
    for (index in 0..4) {
        val y = h * 0.47f + (index * 12.dp.toPx())
        drawLine(
            color = cropLineColor,
            start = Offset(w * 0.07f, y),
            end = Offset(w * 0.35f, y + 5.dp.toPx()),
            strokeWidth = 1.5.dp.toPx(),
            cap = StrokeCap.Round
        )
        drawLine(
            color = cropLineColor,
            start = Offset(w * 0.63f, y + 4.dp.toPx()),
            end = Offset(w * 0.94f, y - 2.dp.toPx()),
            strokeWidth = 1.5.dp.toPx(),
            cap = StrokeCap.Round
        )
    }

    drawOval(
        brush = Brush.linearGradient(
            colors = listOf(WireSkyPale, WireSky.copy(alpha = 0.66f)),
            start = Offset(w * 0.05f, h * 0.73f),
            end = Offset(w * 0.28f, h * 0.92f)
        ),
        topLeft = Offset(w * 0.04f, h * 0.70f),
        size = Size(w * 0.27f, h * 0.18f)
    )
    drawArc(
        color = WireWhite.copy(alpha = 0.72f),
        startAngle = 190f,
        sweepAngle = 150f,
        useCenter = false,
        topLeft = Offset(w * 0.08f, h * 0.75f),
        size = Size(w * 0.18f, h * 0.07f),
        style = androidx.compose.ui.graphics.drawscope.Stroke(width = 1.5.dp.toPx())
    )

    val fencePath = Path().apply {
        moveTo(w * 0.03f, h * 0.32f)
        lineTo(w * 0.35f, h * 0.32f)
        lineTo(w * 0.36f, h * 0.64f)
        moveTo(w * 0.63f, h * 0.31f)
        lineTo(w * 0.96f, h * 0.31f)
        lineTo(w * 0.96f, h * 0.64f)
    }
    drawPath(
        path = fencePath,
        color = WireSage.copy(alpha = 0.30f),
        style = androidx.compose.ui.graphics.drawscope.Stroke(
            width = 1.5.dp.toPx(),
            pathEffect = PathEffect.dashPathEffect(floatArrayOf(8.dp.toPx(), 6.dp.toPx()))
        )
    )

    drawMapTree(Offset(w * 0.31f, h * 0.17f), 0.8f)
    drawMapTree(Offset(w * 0.57f, h * 0.16f), 0.65f)
    drawMapTree(Offset(w * 0.89f, h * 0.75f), 0.9f)
    drawMapTree(Offset(w * 0.34f, h * 0.84f), 0.7f)
}

private fun androidx.compose.ui.graphics.drawscope.DrawScope.drawMapTree(
    center: Offset,
    scale: Float
) {
    val trunkHeight = 12.dp.toPx() * scale
    drawLine(
        color = WireSoil.copy(alpha = 0.78f),
        start = center + Offset(0f, 5.dp.toPx() * scale),
        end = center + Offset(0f, trunkHeight),
        strokeWidth = 2.dp.toPx() * scale,
        cap = StrokeCap.Round
    )
    drawCircle(
        color = WireSageDeep.copy(alpha = 0.72f),
        radius = 9.dp.toPx() * scale,
        center = center + Offset(-5.dp.toPx() * scale, 0f)
    )
    drawCircle(
        color = WireSage.copy(alpha = 0.78f),
        radius = 11.dp.toPx() * scale,
        center = center + Offset(4.dp.toPx() * scale, -2.dp.toPx() * scale)
    )
    drawCircle(
        color = WireLeaf.copy(alpha = 0.72f),
        radius = 7.dp.toPx() * scale,
        center = center + Offset(0f, -8.dp.toPx() * scale)
    )
}
