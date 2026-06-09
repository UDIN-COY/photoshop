import React, { useState } from 'react';
import { SlidersHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';
import { useTranslation } from 'react-i18next';

export type ToolCategory = 'adjust' | 'geometry' | 'color' | 'filters' | 'restore' | 'segment' | 'compress' | null;

interface SidebarProps {
  activeCategory: ToolCategory;
  onApplyTool: (endpoint: string, params?: Record<string, string | number>) => void;
  isProcessing: boolean;
  disabled: boolean;
}

export default function Sidebar({ activeCategory, onApplyTool, isProcessing, disabled }: SidebarProps) {
  const { t } = useTranslation();

  // Enhancement
  const [brightness, setBrightness] = useState(0);
  const [contrast, setContrast] = useState(0);
  const [smoothType, setSmoothType] = useState('gaussian');
  
  // Geometry
  const [rotateAngle, setRotateAngle] = useState(0);
  const [flipMode, setFlipMode] = useState('1'); 
  const [resizeScale, setResizeScale] = useState(1.0);
  const [crop, setCrop] = useState({ x1: 0, y1: 0, x2: 100, y2: 100 });
  const [translate, setTranslate] = useState({ tx: 0, ty: 0 });

  // Filter & Edge
  const [threshVal, setThreshVal] = useState(127);
  const [edgeType, setEdgeType] = useState('canny');
  const [morphType, setMorphType] = useState('erosion');
  const [kernelSize, setKernelSize] = useState(5);

  // Color
  const [hue, setHue] = useState(0);
  const [sat, setSat] = useState(0);
  const [splitChannel, setSplitChannel] = useState('0');

  // Segmentation
  const [kMeansValue, setKMeansValue] = useState(4);

  // Compression
  const [jpegQuality, setJpegQuality] = useState(50);
  const [quantLevels, setQuantLevels] = useState(8);

  const handleApply = (endpoint: string, params: Record<string, string|number> = {}) => {
    if (disabled || isProcessing) return;
    onApplyTool(endpoint, params);
  }

  if (!activeCategory) {
    return (
      <div className="w-[300px] flex-shrink-0 border-l bg-card flex flex-col h-full shadow-sm z-10 p-6 items-center justify-center text-center text-muted-foreground">
        <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center mb-4">
          <SlidersHorizontal className="w-5 h-5 opacity-50" />
        </div>
        <p className="text-sm font-medium text-foreground mb-1">{t('sidebar.empty.title')}</p>
        <p className="text-xs">{t('sidebar.empty.desc')}</p>
      </div>
    );
  }

  let title = '';
  let description = '';
  if (activeCategory === 'adjust') { title = t('sidebar.categories.adjust'); description = t('sidebar.desc.adjust'); }
  if (activeCategory === 'geometry') { title = t('sidebar.categories.geometry'); description = t('sidebar.desc.geometry'); }
  if (activeCategory === 'color') { title = t('sidebar.categories.color'); description = t('sidebar.desc.color'); }
  if (activeCategory === 'filters') { title = t('sidebar.categories.filters'); description = t('sidebar.desc.filters'); }
  if (activeCategory === 'restore') { title = t('sidebar.categories.restore'); description = t('sidebar.desc.restore'); }
  if (activeCategory === 'segment') { title = t('sidebar.categories.segment'); description = t('sidebar.desc.segment'); }
  if (activeCategory === 'compress') { title = t('sidebar.categories.compress'); description = t('sidebar.desc.compress'); }

  return (
    <div className="w-[300px] flex-shrink-0 border-l bg-card flex flex-col h-full shadow-sm z-10">
      <div className="p-4 border-b bg-background sticky top-0 z-20 h-14 flex items-center">
        <div>
          <h2 className="font-semibold text-sm tracking-wide text-foreground uppercase mt-1.5">{title}</h2>
          <p className="text-xs text-muted-foreground mt-0.5">{description}</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        <div className="p-3 space-y-4">
          
          {activeCategory === 'adjust' && (
            <>
              <div className="space-y-4 bg-muted/30 p-4 rounded-xl border border-border/50">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.adjust.brightness')}</Label>
                  <span className="font-mono text-muted-foreground">{brightness}</span>
                </div>
                <Slider min={-100} max={100} step={1} value={[brightness]} onValueChange={(v) => setBrightness(v[0])} disabled={disabled} />
                
                <div className="flex justify-between items-center text-xs mt-4">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.adjust.contrast')}</Label>
                  <span className="font-mono text-muted-foreground">{contrast}</span>
                </div>
                <Slider min={-100} max={100} step={1} value={[contrast]} onValueChange={(v) => setContrast(v[0])} disabled={disabled} />
                
                <Button variant="default" size="sm" className="w-full mt-2" onClick={() => handleApply('/api/enhance/brightness-contrast', { brightness, contrast })}>
                  {t('sidebar.adjust.applySettings')}
                </Button>
              </div>

              <div className="grid grid-cols-2 gap-2 bg-muted/30 p-4 rounded-xl border border-border/50">
                <Button variant="outline" size="sm" onClick={() => handleApply('/api/enhance/equalize')}>{t('sidebar.adjust.equalizeHist')}</Button>
                <Button variant="outline" size="sm" onClick={() => handleApply('/api/enhance/sharpen')}>{t('sidebar.adjust.sharpen')}</Button>
              </div>

              <div className="space-y-4 bg-muted/30 p-4 rounded-xl border border-border/50">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.adjust.blur')}</Label>
                <Select value={smoothType} onValueChange={setSmoothType} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder={t('sidebar.adjust.blurAlgo')} /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="gaussian">{t('sidebar.adjust.gaussianBlur')}</SelectItem>
                    <SelectItem value="average">{t('sidebar.adjust.avgBlur')}</SelectItem>
                    <SelectItem value="median">{t('sidebar.adjust.medianBlur')}</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/enhance/smooth', { ftype: smoothType })}>{t('sidebar.adjust.applyBlur')}</Button>
              </div>
            </>
          )}

          {activeCategory === 'geometry' && (
            <>
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.geometry.rotation')}</Label>
                  <span className="font-mono text-muted-foreground">{rotateAngle}°</span>
                </div>
                <Slider min={-180} max={180} step={1} value={[rotateAngle]} onValueChange={(v) => setRotateAngle(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/rotate', { angle: rotateAngle })}>{t('sidebar.geometry.rotateBtn')}</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.geometry.flipImg')}</Label>
                <Select value={flipMode} onValueChange={setFlipMode} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder={t('sidebar.geometry.flipMode')} /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">{t('sidebar.geometry.flipHorz')}</SelectItem>
                    <SelectItem value="0">{t('sidebar.geometry.flipVert')}</SelectItem>
                    <SelectItem value="-1">{t('sidebar.geometry.flipBoth')}</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/flip', { mode: parseInt(flipMode) })}>{t('sidebar.geometry.flipBtn')}</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.geometry.scale')}</Label>
                  <span className="font-mono text-muted-foreground">{resizeScale.toFixed(2)}x</span>
                </div>
                <Slider min={0.1} max={3.0} step={0.1} value={[resizeScale]} onValueChange={(v) => setResizeScale(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/resize', { scale: resizeScale })}>{t('sidebar.geometry.resizeBtn')}</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.geometry.translation')}</Label>
                <div className="grid grid-cols-2 gap-2">
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="X" value={translate.tx} onChange={e => setTranslate({...translate, tx: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="Y" value={translate.ty} onChange={e => setTranslate({...translate, ty: +e.target.value})} disabled={disabled} />
                </div>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/translate', translate)}>{t('sidebar.geometry.translateBtn')}</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.geometry.cropArea')}</Label>
                <div className="grid grid-cols-2 gap-2">
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="X1" value={crop.x1} onChange={e => setCrop({...crop, x1: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="Y1" value={crop.y1} onChange={e => setCrop({...crop, y1: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="X2" value={crop.x2} onChange={e => setCrop({...crop, x2: +e.target.value})} disabled={disabled} />
                  <Input className="h-8 text-xs font-mono" type="number" placeholder="Y2" value={crop.y2} onChange={e => setCrop({...crop, y2: +e.target.value})} disabled={disabled} />
                </div>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/geom/crop', crop)}>{t('sidebar.geometry.cropBtn')}</Button>
              </div>
            </>
          )}

          {activeCategory === 'restore' && (
            <>
              <div className="space-y-3">
                <Button variant="outline" size="sm" className="w-full justify-start font-normal" onClick={() => handleApply('/api/restore/gaussian')}>
                  {t('sidebar.restore.gaussian')}
                </Button>
                <Button variant="outline" size="sm" className="w-full justify-start font-normal" onClick={() => handleApply('/api/restore/median')}>
                  {t('sidebar.restore.median')}
                </Button>
              </div>
            </>
          )}

          {activeCategory === 'color' && (
            <>
              <div className="bg-muted/30 p-4 rounded-xl border border-border/50">
                <Button variant="outline" size="sm" className="w-full" onClick={() => handleApply('/api/color/grayscale')}>{t('sidebar.color.toGray')}</Button>
              </div>

               <div className="space-y-4 bg-muted/30 p-4 rounded-xl border border-border/50">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.color.extractChannel')}</Label>
                <Select value={splitChannel} onValueChange={setSplitChannel} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder={t('sidebar.color.channel')} /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2">{t('sidebar.color.redChannel')}</SelectItem>
                    <SelectItem value="1">{t('sidebar.color.greenChannel')}</SelectItem>
                    <SelectItem value="0">{t('sidebar.color.blueChannel')}</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/color/split-channel', { channel: parseInt(splitChannel) })}>{t('sidebar.color.extractBtn')}</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground block text-center">
                  {t('sidebar.color.hsvAdj')}
                </Label>
                <div className="flex justify-between items-center text-xs mt-2">
                  <Label className="text-xs text-muted-foreground">{t('sidebar.color.hueShift')}</Label>
                  <span className="font-mono text-muted-foreground">{hue}</span>
                </div>
                <Slider min={-180} max={180} step={1} value={[hue]} onValueChange={(v) => setHue(v[0])} disabled={disabled} />
                
                <div className="flex justify-between items-center text-xs mt-3">
                  <Label className="text-xs text-muted-foreground">{t('sidebar.color.sat')}</Label>
                  <span className="font-mono text-muted-foreground">{sat}</span>
                </div>
                <Slider min={-255} max={255} step={1} value={[sat]} onValueChange={(v) => setSat(v[0])} disabled={disabled} />
                
                <Button variant="secondary" size="sm" className="w-full mt-2" onClick={() => handleApply('/api/color/hsv-adjust', { hue_shift: hue, sat_shift: sat })}>{t('sidebar.color.applyHsv')}</Button>
              </div>
            </>
          )}

          {activeCategory === 'filters' && (
            <>
              <div className="space-y-4">
                <div className="flex justify-between items-center text-xs">
                  <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.filters.threshold')}</Label>
                  <span className="font-mono text-muted-foreground">{threshVal}</span>
                </div>
                <Slider min={0} max={255} step={1} value={[threshVal]} onValueChange={(v) => setThreshVal(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/edge/threshold', { thresh_val: threshVal })}>{t('sidebar.filters.applyThresh')}</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.filters.edgeAlgo')}</Label>
                <Select value={edgeType} onValueChange={setEdgeType} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder={t('sidebar.filters.algo')} /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="canny">Canny</SelectItem>
                    <SelectItem value="sobel">Sobel</SelectItem>
                    <SelectItem value="prewitt">Prewitt</SelectItem>
                    <SelectItem value="robert">Robert</SelectItem>
                    <SelectItem value="laplacian">Laplacian</SelectItem>
                    <SelectItem value="log">Laplacian of Gaussian</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/edge/detect', { etype: edgeType })}>{t('sidebar.filters.detectEdge')}</Button>
              </div>

              <Separator />

              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.filters.morphology')}</Label>
                <Select value={morphType} onValueChange={setMorphType} disabled={disabled}>
                  <SelectTrigger className="h-8 text-xs"><SelectValue placeholder={t('sidebar.filters.operation')} /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="erosion">{t('sidebar.filters.erosion')}</SelectItem>
                    <SelectItem value="dilation">{t('sidebar.filters.dilation')}</SelectItem>
                    <SelectItem value="opening">{t('sidebar.filters.opening')}</SelectItem>
                    <SelectItem value="closing">{t('sidebar.filters.closing')}</SelectItem>
                  </SelectContent>
                </Select>
                
                <div className="flex justify-between items-center text-xs mt-3">
                  <Label className="text-xs text-muted-foreground">{t('sidebar.filters.kernelSize')}</Label>
                  <span className="font-mono text-muted-foreground">{kernelSize}x{kernelSize}</span>
                </div>
                <Slider min={1} max={21} step={2} value={[kernelSize]} onValueChange={(v) => setKernelSize(v[0])} disabled={disabled} />
                
                <Button variant="secondary" size="sm" className="w-full mt-2" onClick={() => handleApply('/api/morphology', { mtype: morphType, kernel_size: kernelSize })}>{t('sidebar.filters.applyMorph')}</Button>
              </div>
            </>
          )}

          {activeCategory === 'segment' && (
            <>
              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.segment.kmeans')}</Label>
                <div className="flex justify-between items-center text-xs mt-1">
                  <span className="text-xs text-muted-foreground">{t('sidebar.segment.kCount')}</span>
                  <span className="font-mono text-muted-foreground">{kMeansValue}</span>
                </div>
                <Slider min={2} max={16} step={1} value={[kMeansValue]} onValueChange={(v) => setKMeansValue(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/segment/kmeans', { k: kMeansValue })}>{t('sidebar.segment.applyKmeans')}</Button>
              </div>

              <Separator />
              
              <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground block">{t('sidebar.segment.otherMethods')}</Label>
              <div className="space-y-2 mt-4">
                <Button variant="outline" size="sm" className="w-full justify-start font-normal" onClick={() => handleApply('/api/segment/edge-based')}>{t('sidebar.segment.edgeBased')}</Button>
                <Button variant="default" size="sm" className="w-full justify-start font-medium" onClick={() => handleApply('/api/ml/detect-objects')}>
                  {t('sidebar.segment.detectCnn')}
                </Button>
              </div>
            </>
          )}

          {activeCategory === 'compress' && (
            <>
              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.compress.jpegSim')}</Label>
                <div className="flex justify-between items-center text-xs mt-1">
                  <span className="text-xs text-muted-foreground">{t('sidebar.compress.quality')}</span>
                  <span className="font-mono text-muted-foreground">{jpegQuality}%</span>
                </div>
                <Slider min={1} max={100} step={1} value={[jpegQuality]} onValueChange={(v) => setJpegQuality(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/compress/simulate', { quality: jpegQuality })}>{t('sidebar.compress.applyJpeg')}</Button>
              </div>

              <Separator />
              
              <div className="space-y-4">
                <Label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{t('sidebar.compress.quantization')}</Label>
                <div className="flex justify-between items-center text-xs mt-1">
                  <span className="text-xs text-muted-foreground">{t('sidebar.compress.levels')}</span>
                  <span className="font-mono text-muted-foreground">{quantLevels}</span>
                </div>
                <Slider min={2} max={64} step={2} value={[quantLevels]} onValueChange={(v) => setQuantLevels(v[0])} disabled={disabled} />
                <Button variant="secondary" size="sm" className="w-full" onClick={() => handleApply('/api/compress/quantize', { levels: quantLevels })}>{t('sidebar.compress.applyQuant')}</Button>
              </div>
            </>
          )}

        </div>
      </div>
    </div>
  );
}
