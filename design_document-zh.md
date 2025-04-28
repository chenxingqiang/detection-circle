# 圆形检测与圆度计算 - 设计文档

## 项目概述
本项目旨在检测产品图像中的圆形并计算其圆度公差。圆度是指工件的横截面接近理论圆的程度，最大半径与最小半径之差即为圆度误差。

## 需求
1. 提取产品图像轮廓
2. 实现轮廓单线化处理
3. 实现单线化轮廓的几何描述
4. 计算关键圆的圆度公差

## 技术方案

### 1. 图像处理流程
1. **图像加载**：从数据集加载图像
2. **预处理**：
   - 转换为灰度图
   - 应用高斯模糊减少噪声
   - 应用阈值处理/边缘检测突出边缘
3. **轮廓检测**：从处理后的图像中提取轮廓
4. **轮廓过滤**：基于形状属性过滤轮廓以识别潜在的圆形
5. **单线化处理**：将轮廓转换为单线表示
6. **圆形拟合**：对过滤后的轮廓拟合圆形
7. **圆度计算**：使用需求中描述的四种方法之一计算圆度公差

### 2. 圆度计算方法
根据需求规定，我们将实现以下四种圆度误差评定方法：
1. **最小区域法**：找到两个同心圆，使其径向差最小且包含所有点
2. **最小二乘圆法**：找到一个圆，使点到圆的距离平方和最小
3. **最小外接圆法**：对于外圆，找到包含所有点的最小圆
4. **最大内接圆法**：对于内圆，找到被所有点包含的最大圆

### 3. 可视化
- 显示带有检测轮廓的原始图像
- 突出显示检测到的圆形
- 可视化圆度计算（内外同心圆）
- 显示数值结果（圆度公差值）

## 组件设计

### 1. ImageProcessor类
负责加载和预处理图像：
- `load_image(path)`：从文件加载图像
- `preprocess(image)`：应用预处理步骤
- `detect_edges(image)`：应用边缘检测
- `extract_contours(image)`：从处理后的图像中提取轮廓

### 2. ContourProcessor类
负责处理和过滤轮廓：
- `filter_contours(contours)`：基于形状属性过滤轮廓
- `single_line_processing(contour)`：将轮廓转换为单线表示

### 3. CircleDetector类
负责检测圆形并计算属性：
- `detect_circles(contours)`：从轮廓中检测圆形
- `fit_circle(points)`：对一组点拟合圆形

### 4. RoundnessCalculator类
负责计算圆度公差：
- `min_zone_method(points)`：使用最小区域法计算圆度
- `least_squares_method(points)`：使用最小二乘法计算圆度
- `min_circumscribed_method(points)`：使用最小外接圆法计算圆度
- `max_inscribed_method(points)`：使用最大内接圆法计算圆度

### 5. Visualizer类
负责可视化：
- `display_image(image)`：显示图像
- `draw_contours(image, contours)`：在图像上绘制轮廓
- `draw_circles(image, circles)`：在图像上绘制圆形
- `visualize_roundness(image, inner_circle, outer_circle)`：可视化圆度计算

## 数据流
1. 加载图像 → ImageProcessor
2. 预处理图像 → ImageProcessor
3. 提取轮廓 → ImageProcessor
4. 过滤轮廓 → ContourProcessor
5. 单线化处理 → ContourProcessor
6. 检测圆形 → CircleDetector
7. 计算圆度 → RoundnessCalculator
8. 可视化结果 → Visualizer

## 测试计划
1. 各组件的单元测试
2. 完整流程的集成测试
3. 使用已知圆度值的样本图像进行验证测试